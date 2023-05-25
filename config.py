import os
import dotenv
from pymongo import MongoClient
from telethon import TelegramClient

dotenv.load_dotenv(".env")

api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
db_url = os.environ.get('MONGO_DB_URL')
FILES_CHANNEL = int(os.environ.get('FILES_CHANNEL'))
LOGS_CHANNEL = int(os.environ.get('LOGS_CHANNEL'))
LINKS_CHANNEL = int(os.environ.get('LINKS_CHANNEL'))
FILES_HIDER_BOT_USERNAME = os.environ.get('FILES_HIDER_BOT_USERNAME')


client = MongoClient(db_url, tls=True)

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
