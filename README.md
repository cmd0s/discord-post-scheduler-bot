# Discord Post Scheduler Bot

This bot is designed to automatically post messages in a specific Discord channel according to a predefined schedule. It takes messages from Markdown files located in the `posts` directory, which are named based on the desired posting date and time. The bot then moves these files to the `published` directory after successfully posting.

## Features
- Automatically posts messages from a `posts` folder to a Discord channel based on the date and time in the filename.
- Files are moved to the `published` directory after they are successfully posted.
- Skips files that are older than 3 minutes to ensure only relevant posts are shared.

## Requirements
- Python 3.8+ installed on your system.
- Discord account and a bot token from the Discord Developer Portal.
- The `discord.py` library.

## Setup and Installation

### 1. Clone the Repository
First, clone the repository to your local machine:
```sh
git clone [<repository-url>](https://github.com/cmd0s/discord-post-scheduler-bot.git)
cd discord-post-scheduler-bot
```

### 2. Create a Virtual Environment
Create a virtual environment to isolate the bot's dependencies:
```sh
python -m venv venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment:
- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On Linux/macOS:
  ```sh
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install the required dependencies from `requirements.txt`:
```sh
pip install -r requirements.txt
```

### 5. Set Up a Bot on Discord
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** to create a new application and give it a name.
3. Navigate to the **Bot** tab and click **Add Bot**.
4. Copy the TOKEN and save it. This token will be used to authenticate the bot.   
   (If you cannot find the token, click Reset Token to generate a new one.)
5. Under **Privileged Gateway Intents**, enable **Message Content Intent**.

### 6. Invite the Bot to Your Server
1. Go to the **OAuth2** tab and click on **URL Generator**.
2. Select the **bot** scope.
3. Under **Bot Permissions**, select appropriate permissions, such as **Send Messages**.
4. Copy the generated URL and paste it into your browser to invite the bot to your server.

### 7. Configure the Bot
Replace `YOUR_DISCORD_TOKEN` in `bot.py` with the token you obtained earlier.
Ensure that the server name (`SERVER_NAME`) and channel name (`CHANNEL_NAME`) in the script match the server and channel where you want the bot to post.

### 8. Running the Bot
Run the bot using the following command:
```sh
python bot.py
```

To keep the bot running indefinitely, you can use a `screen` session:
```sh
screen -S discord_bot
python bot.py
```
Press `Ctrl + A` then `D` to detach from the screen session and keep the bot running in the background.

## How the Bot Works
- The bot monitors the `posts` directory for Markdown (`.md`) files named using the format `DDMMYYYY-HHMM.md`.
  - `DD` - Day of the month.
  - `MM` - Month.
  - `YYYY` - Year.
  - `HHMM` - Time (24-hour format).
- When the date and time in the filename match or are before the current time, the bot posts the content of the file to the specified channel.
- After posting, the bot moves the file to the `published` directory to keep the `posts` directory clean.
- Files older than 3 minutes that haven't been posted are skipped to avoid outdated messages.

## Notes
- Place Markdown files in the `posts` directory for the bot to post.
- Ensure the filenames are properly formatted (`DDMMYYYY-HHMM.md`), as the bot uses the filename to determine when to post.
- The `published` directory stores all the successfully posted messages.

Feel free to customize the bot's settings to match your requirements, such as adjusting the post frequency or adding more features to interact with users on your server.

