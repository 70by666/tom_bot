import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from dotenv import find_dotenv, load_dotenv
import openai

# config

load_dotenv(find_dotenv())

storage = MemoryStorage()

bot = Bot(str(os.getenv('BOT_TOKEN')))

dp = Dispatcher(bot, storage=storage)

WHITELIST = str(os.getenv('WHITELIST')).split()

OPEN_AI_TOKEN = str(os.getenv('CHATGPT_TOKEN'))

SUPERUSER_API_LOGIN = str(os.getenv('SUPERUSER_API_LOGIN'))
SUPERUSER_API_PASSWORD = str(os.getenv('SUPERUSER_API_PASSWORD'))