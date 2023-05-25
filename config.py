import os
from pymongo import MongoClient
from telethon import TelegramClient



# api_id = os.environ.get('API_ID')
# api_hash = os.environ.get('API_HASH')
# bot_token = os.environ.get('BOT_TOKEN')
# db_url = os.environ.get('MONGO_DB_URL')
# FILES_CHANNEL = os.environ.get('FILES_CHANNEL')
# LOGS_CHANNEL = os.environ.get('LOGS_CHANNEL')
# LINKS_CHANNEL = os.environ.get('LINKS_CHANNEL')
# FILES_HIDER_BOT_USERNAME = os.environ.get('FILES_HIDER_BOT_USERNAME')

api_id = 23803153
api_hash = '98a8f28bff15101c3c0a076513c27caa'
bot_token = '5809203660:AAHYRNh0qdUqyQ--UIK-hju_unb23B1_BvI'
db_url = 'mongodb+srv://od3n:od3n@cluster0.suttmyz.mongodb.net/?retryWrites=true&w=majority'
FILES_CHANNEL = -1001788241255
LOGS_CHANNEL = -1001855312135
LINKS_CHANNEL = -1001793416773
FILES_HIDER_BOT_USERNAME = 'Lasyassnowork_bot'


client = MongoClient(db_url, tls=True)

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
