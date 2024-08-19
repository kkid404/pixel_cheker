from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_IDS = os.getenv('CHAT_IDS').split(',')