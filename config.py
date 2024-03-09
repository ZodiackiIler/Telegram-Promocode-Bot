# инициализируем необзходимые библиотеки
from dotenv import load_dotenv
import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

load_dotenv()

TOKEN_BOT = os.getenv("TOKEN_BOT")
USERNAME_BOT = os.getenv("USERNAME_BOT")

ADMIN_ID = os.getenv("ADMIN_ID")
LOGS_CHAT_ID = os.getenv("LOGS_CHAT_ID")

SQLITE3_CONNECT = os.getenv("SQLITE3_CONNECT")

DATABASE_TYPE = ('sqlite3')

start_message_for_user = f"""
<b>Приветствую тебя, дорогой друг!</b>
Я - Бот для активации промокодов, и предназначен для оптимизации выдаче призов с помощью промокодов.
Если ты перешел не по ссылке для активации промокода, но он у тебя есть, то можешь воспользоваться командой <code>/activate `promocode`</code> и активировать его.
"""

start_message_for_admin = f"""
<b>Приветствую тебя, дорогой администратор!</b>
Я - Бот для активации промокодов, и предназначен для оптимизации выдаче призов с помощью промокодов.
Если ты хочешь создать новый промокод, то можешь воспользоваться командой, чтобы создать его <code>/create `promocode` `balance` `count` `description`</code>, причем `description` может быть пустым.
"""

# Объект бота
bot = Bot(TOKEN_BOT);
# Диспетчер
dp = Dispatcher(bot, storage=storage)
