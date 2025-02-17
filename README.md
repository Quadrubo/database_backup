# database_backup

> [!CAUTION]
> This project has been superseded by using [borgmatic](https://github.com/borgmatic-collective/borgmatic).

This is the script I use to backup my databases running in docker containers on my Unraid server.
After backup them up to the location specified in the `.env` file, the backup is further processed by [Duplicati](https://github.com/duplicati/duplicati).

## Usage in the User Scripts plugin

1. Navigate to `/boot/config/plugins/user.scripts/scripts/`
2. Clone the repository with `git clone https://github.com/Quadrubo/database_backup`
3. Copy the environment file and edit it to match your system `cp .env.example .env`
4. Edit the variable `ENV_FILE_PATH` in the first rows of the `script` to match your newly created `.env` file
5. Copy the containers file and edit it to match your system `cp containers.json.example containers.json`
6. Run the script in Unraid under `Settings -> User Scripts`. You can even schedule it to run daily.

## General Usage

1. Follow the steps 1 - 5 outlined in [Usage in the User Scripts plugin](#usage-in-the-user-scripts-plugin) but clone the repository to anywhere you like. You can skip step 5 if you know your system supports `.env` file loading.
2. Run the script using `python ./script`

## Notifications

You can use [Ntfy](https://github.com/binwiederhier/ntfy) to get notifications when your script has finished executing.
Edit the `ENABLE_NTFY`, `NTFY_URI` and `NTFY_BEARER` variables to enable notifications.
