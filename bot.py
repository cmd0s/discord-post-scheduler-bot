import discord
from discord.ext import tasks, commands
import os
import datetime
import asyncio
import logging

# Bot settings
TOKEN = 'YOUR_DISCORD_TOKEN'
SERVER_NAME = 'YourServerName'
CHANNEL_NAME = 'your-channel-name'
POSTS_DIRECTORY = 'posts'
PUBLISHED_DIRECTORY = 'published'

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s', handlers=[
    logging.FileHandler("log.txt"),
    logging.StreamHandler()
])

# Bot initialization
discord.VoiceClient.warn_nacl = False
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True  # Add this line to enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    # Find the appropriate channel on the server
    for guild in bot.guilds:
        if guild.name == SERVER_NAME:
            for channel in guild.text_channels:
                if channel.name == CHANNEL_NAME:
                    bot.tip_channel = channel
                    break
    if hasattr(bot, 'tip_channel'):
        monitor_posts.start()  # Start periodic task
    else:
        logging.error(f'Channel \"{CHANNEL_NAME}\" not found on server \"{SERVER_NAME}\"')


@bot.event
async def on_disconnect():
    logging.info('Bot has disconnected')


@tasks.loop(seconds=60)
async def monitor_posts():
    current_time = datetime.datetime.now()
    files = os.listdir(POSTS_DIRECTORY)

    for file in files:
        if file.endswith('.md'):
            file_datetime_str = file.replace('.md', '')
            try:
                file_datetime = datetime.datetime.strptime(file_datetime_str, '%d%m%Y-%H%M')
                time_difference = current_time - file_datetime
                if time_difference.total_seconds() > 180:
                    logging.info(f'Skipping old file: {file}')
                    continue
                if file_datetime <= current_time:
                    file_path = os.path.join(POSTS_DIRECTORY, file)

                    # Read the content and post it to the Discord channel
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Send the content to the Discord channel
                        await bot.tip_channel.send(content)

                        # Move the file to the 'published' directory
                        published_filepath = os.path.join(PUBLISHED_DIRECTORY, file)
                        os.rename(file_path, published_filepath)

                        logging.info(f'Post published from file: {file}')

                    except Exception as e:
                        logging.error(f'Error while publishing file {file}: {e}')

            except ValueError:
                logging.warning(f'Invalid file name format: {file}')


try:
    bot.run(TOKEN)
except Exception as e:
    logging.error(f'Bot failed to start: {e}')
