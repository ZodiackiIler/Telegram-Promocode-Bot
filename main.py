# инициализируем необзходимые библиотеки
from aiogram.utils import executor
from aiogram.utils import markdown
from config import dp, bot, LOGS_CHAT_ID, ADMIN_ID, start_message_for_user, start_message_for_admin, USERNAME_BOT
from db import db
from aiogram import Dispatcher, types
from aiogram.types import Message, ParseMode
from aiogram.dispatcher import FSMContext

########################################
#
#           Начало работы бота
#
########################################

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    start_command = message.text
    promocode_id = start_command[7:]
    if promocode_id == None or promocode_id == '':
        if user_id != int(ADMIN_ID):
            await bot.send_message(user_id, start_message_for_user, parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(user_id, start_message_for_admin, parse_mode=ParseMode.HTML)
    else:
        if db.promocode_exists(promocode_id):
            promocode = db.get_promocode(promocode_id)
            balance = promocode[2]
            if db.user_activates(user_id, promocode_id):
                await bot.send_message(user_id, "Вы уже активировали промокод")
            elif user_id == int(ADMIN_ID):
                await bot.send_message(user_id, "Вы не можете активировать промокод, так как вы администратор")
            else:
                if db.activate_enable(promocode_id) == '1':
                    if message.from_user.username == None:
                        await bot.send_message(user_id, "У вас нету username, пожалуйста, установите его, для возможности активации промокода")
                    else:
                        await bot.send_message(user_id, f"Вы успешно активировали промокод на {balance} и скоро Администратор выдаст вам приз")
                        await bot.send_message(LOGS_CHAT_ID, f"Пользователь @{message.from_user.username} ({user_id}) активировал промокод {promocode_id} на {balance}")
                        db.promo_active_count_add(promocode_id)
                        db.deactivate_promocode_if_count(promocode_id)
                        db.add_active_promocode(user_id, promocode_id)
                else:
                    await bot.send_message(user_id, "Промокод полностью активирован")
        else:
            await bot.send_message(user_id, "Промокод не найден")

@dp.message_handler(commands=['activate'])
async def activate(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    args = message.get_args().split()
    if len(args) == 1:
        promocode_id = args[0]
        if db.promocode_exists(promocode_id):
            promocode = db.get_promocode(promocode_id)
            balance = promocode[2]
            if db.user_activates(user_id, promocode_id):
                await bot.send_message(user_id, "Вы уже активировали промокод")
            elif user_id == int(ADMIN_ID):
                await bot.send_message(user_id, "Вы не можете активировать промокод, так как вы администратор")
            else:
                if db.activate_enable(promocode_id) == 'True':
                    if message.from_user.username == None:
                        await bot.send_message(user_id, "У вас нету username, пожалуйста, установите его, для возможности активации промокода")
                    else:
                        await bot.send_message(user_id, f"Вы успешно активировали промокод на {balance} и скоро Администратор выдаст вам приз")
                        await bot.send_message(LOGS_CHAT_ID, f"Пользователь @{message.from_user.username} ({user_id}) активировал промокод {promocode_id} на {balance}")
                        db.promo_active_count_add(promocode_id)
                        db.deactivate_promocode_if_count(promocode_id)
                        db.add_active_promocode(user_id, promocode_id)
                else:
                    await bot.send_message(user_id, "Промокод полностью активирован")
        else:
            await bot.send_message(user_id, "Промокод не найден")
    else:
        await bot.send_message(user_id, "Пожалуйста, введите промокод для активации /activate `promocode`")

@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    args = message.get_args().split()
    if user_id == int(ADMIN_ID):
        if len(args) >= 4: 
            promocode_id = args[0]
            balance = args[1]
            count = args[2]
            description = ' '.join(args[3:])  
            if db.promocode_exists(promocode_id):
                await bot.send_message(user_id, "Промокод уже существует")
            else:
                db.add_promocode(promocode_id, balance, count, description)
                await bot.send_message(user_id, f"Промокод успешно создан.\nНазвание: <code>{promocode_id}</code>\nСумма: <b>{balance}</b>\nКоличество: <b>{count}</b>\nОписание: <b>{description}</b>\n\n<b>Ссылочка для активации</b>: <code>https://t.me/{USERNAME_BOT}?start={promocode_id}</code>", parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(user_id, "Пожалуйста, введите данные для создания промокода /create `promocode` `balance` `count` `description`")
    else:
        pass

@dp.message_handler(commands=['deactivate'])
async def deactivate(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    args = message.get_args().split()
    if user_id == int(ADMIN_ID):
        if len(args) == 1:
            promocode_id = args[0]
            if db.promocode_exists(promocode_id) and db.activate_enable(promocode_id):
                db.deactivate_promocode(promocode_id)
                await bot.send_message(user_id, "Промокод успешно деактивирован")
            else:
                await bot.send_message(user_id, "Промокод не найден")
        else:
            await bot.send_message(user_id, "Пожалуйста, введите промокод для удаления /deactivate `promocode`")
    else:
        pass

#################################
#           запуск бота         #
#################################
    
async def on_startup(_):
    print(f'{USERNAME_BOT} вышел в онлайн')

async def on_shutdown(_):
    print(f'{USERNAME_BOT} вышел из онлайна')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
