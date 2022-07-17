from aiogram import Dispatcher, Bot, types
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


load_dotenv()

api = os.getenv('API_KEY')
path = f'&api_key={api}'

bot_token = os.getenv('TOKEN')
bot = Bot(bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())