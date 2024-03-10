# инициализируем необзходимые библиотеки
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

admin_menu = InlineKeyboardMarkup(resize_keyboard=True)
statsbtn = InlineKeyboardButton("Статистика", callback_data="statsbtn")
infobtn = InlineKeyboardButton("Информация", callback_data="infobtn")
logs_linkbtn = InlineKeyboardButton("Чат с логами", url="YOU_CHAT_LOG_ID")
admin_menu.row(statsbtn, infobtn).add(logs_linkbtn)
