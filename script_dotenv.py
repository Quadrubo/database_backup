#!/usr/bin/python3.9
import subprocess
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import requests

load_dotenv()

JSON_FILE_NAME = os.getenv("JSON_FILE_NAME")
TMP_FOLDER = os.getenv("TMP_FOLDER")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER")

ENABLE_NTFY = os.getenv("ENABLE_NTFY").lower() == 'true'
NTFY_URI = os.getenv("NTFY_URI")
NTFY_BEARER = os.getenv("NTFY_BEARER")

with open(JSON_FILE_NAME, 'r') as f:
    container_json = json.load(f)["containers"]

if not os.path.exists(TMP_FOLDER):
    os.mkdir(TMP_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

file_names = []

def gzip_sql_files(files):
    output_file_name = datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + "_db_backup.tar.gz"

    command = f"tar --remove-files -czf {OUTPUT_FOLDER}/{output_file_name} -C {TMP_FOLDER} " + " ".join(files)

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    p.wait()

    print(f"Database backup written to \"{OUTPUT_FOLDER}/{output_file_name}\".")

def send_ntfy():
    container_names = ', '.join(container['container_name'] for container in container_json)

    requests.post(
        NTFY_URI, 
        data=f"Containers: {container_names}",
        headers={
            "Title": "Database backup successful :)",
            "Authorization": f"Bearer {NTFY_BEARER}"
        }
    )

class Database:
    def __init__(self, container_name) -> None:
        self.container_name = container_name

    def get_container_connection_string(self, interactive=False):
        if interactive:
            return f"docker exec -i {self.container_name}"
        else:
            return f"docker exec {self.container_name}"
        
    def dump(self):
        raise NotImplementedError
    
class Mariadb(Database):
    def __init__(self, container_name, user, password) -> None:
        super().__init__(container_name)
        self.user = user
        self.password = password
        self.databases = []

    def get_dump_command(self, database_name):
        return f"{super().get_container_connection_string()} mysqldump -u {self.user} -p{self.password} {database_name}"

    def dump_to_file(self):
        file_names = []

        for database in self.databases:
            dump_command = f"{self.get_dump_command(database)} > {TMP_FOLDER}/{self.container_name}_{database}.sql"

            sql_dumper = subprocess.Popen(dump_command, stdout=subprocess.PIPE, shell=True)
            sql_dumper.wait()

            file_names.append(f"{self.container_name}_{database}.sql")

        return file_names

    def fill_databases(self):
        command = f"echo 'show databases;' | {super().get_container_connection_string(interactive=True)} mysql --user={self.user} --password={self.password} | grep -v Database | grep -v information_schema | grep -v mysql | grep -v performance_schema"

        self.databases = subprocess.check_output(command, shell=True).decode("utf-8").splitlines()

    def dump(self):
        self.fill_databases()

        file_names = self.dump_to_file()

        return file_names

class Postgresql(Database):
    def __init__(self, container_name, user) -> None:
        super().__init__(container_name)  
        self.user = user

    def get_dump_command(self):
        return f"{super().get_container_connection_string()} pg_dumpall -c -U {self.user}"

    def dump_to_file(self):
        dump_command = f"{self.get_dump_command()} > {TMP_FOLDER}/{self.container_name}.sql"

        sql_dumper = subprocess.Popen(dump_command, stdout=subprocess.PIPE, shell=True)
        sql_dumper.wait()

        return f"{self.container_name}.sql"

    def dump(self):
        file_names = [self.dump_to_file()]

        return file_names

for container in container_json:
    container_name = container["container_name"]
    database_type = container["database_type"]
    root_password = container["root_password"]

    if database_type in ["mariadb"]:
        database = Mariadb(
            container_name=container_name,
            user="root",
            password=root_password
        )
    elif database_type in ["postgresql"]:
        database = Postgresql(
            container_name=container_name,
            user="postgres",
        )

    file_names.extend(database.dump())

gzip_sql_files(file_names)

if ENABLE_NTFY:
    send_ntfy()
