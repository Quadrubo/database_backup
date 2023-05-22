# database_backup

This is the script I use to backup my databases running in docker containers on my Unraid server.

## Usage in the User Scripts plugin

1. Navigate to `/boot/config/plugins/user.scripts/scripts/`
2. Clone the repository with `git clone https://github.com/Quadrubo/database_backup`
3. Copy the script so it's recognized by the plugin `cp script_default.py script`
4. Copy the containers file and edit it to match your system `cp containers.json.example containers.json`
5. Edit the variables in the first rows of the `script` to match your system.

## Usage with dotenv

The User Scripts plugin doesn't support using environment variables.
This is a guide on how to setup the other version which uses environment variables.

1. Clone the repository with `git clone https://github.com/Quadrubo/database_backup`
2. Copy the script so it's recognized by the plugin `cp script_dotenv.py script`
3. Copy the containers file and edit it to match your system `cp containers.json.example containers.json`
4. Copy the environment file and edit it to match your system `cp .env.example .env`
5. Edit the variables in the `.env` to match your system.
