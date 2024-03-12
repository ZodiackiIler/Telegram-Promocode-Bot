# инициализируем необзходимые библиотеки
from aiogram.utils import executor
from aiogram.utils import markdown
from config import dp, bot, LOGS_CHAT_ID, ADMIN_ID, start_message_for_user, start_message_for_admin, USERNAME_BOT, info_commands_admin
from db import db
from aiogram import Dispatcher, types
from aiogram.types import Message, ParseMode
from markup import admin_menu
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
            await bot.send_message(user_id, start_message_for_admin, parse_mode=ParseMode.HTML, reply_markup=admin_menu)
    else:
        if db.promocode_exists(promocode_id):
            promocode = db.get_promocode(promocode_id)
            balance = promocode[2]
            coins = promocode[4]
            if db.user_activates(user_id, promocode_id):
                await bot.send_message(user_id, "Вы уже активировали промокод")
            elif user_id == int(ADMIN_ID):
                await bot.send_message(user_id, "Вы не можете активировать промокод, так как вы администратор")
            else:
                if db.activate_enable(promocode_id) == '1':
                    if message.from_user.username == None:
                        await bot.send_message(user_id, "У вас нету username, пожалуйста, установите его, для возможности активации промокода")
                    else:
                        await bot.send_message(user_id, f"Вы успешно активировали промокод на {balance} {coins} и скоро Администратор выдаст вам приз")
                        await bot.send_message(LOGS_CHAT_ID, f"Пользователь @{message.from_user.username} ({user_id}) активировал промокод {promocode_id} на {balance} {coins}")
                        db.promo_active_count_add(promocode_id)
                        db.add_active_promocode(user_id, message.from_user.username, promocode_id)
                        db.deactivate_promocode_if_count(promocode_id)
                else:
                    await bot.send_message(user_id, "Промокод полностью активирован")
        else:
            await bot.send_message(user_id, "Промокод не найден")

@dp.message_handler(commands=['activate'])
async def activate(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().split()
    if len(args) >= 1:
        promocode_id = args[0]
        if db.promocode_exists(promocode_id):
            promocode = db.get_promocode(promocode_id)
            balance = promocode[2]
            coins = promocode[4]
            if db.user_activates(user_id, promocode_id):
                await bot.send_message(user_id, "Вы уже активировали промокод")
            elif user_id == int(ADMIN_ID):
                await bot.send_message(user_id, "Вы не можете активировать промокод, так как вы администратор")
            else:
                if db.activate_enable(promocode_id) == '1':
                    if message.from_user.username == None:
                        await bot.send_message(user_id, "У вас нету username, пожалуйста, установите его, для возможности активации промокода")
                    else:
                        await bot.send_message(user_id, f"Вы успешно активировали промокод на {balance} {coins} и скоро Администратор выдаст вам приз")
                        await bot.send_message(LOGS_CHAT_ID, f"Пользователь @{message.from_user.username} ({user_id}) активировал промокод {promocode_id} на {balance} {coins}")
                        db.promo_active_count_add(promocode_id)
                        db.add_active_promocode(user_id, message.from_user.username, promocode_id)
                        db.deactivate_promocode_if_count(promocode_id)
                else:
                    await bot.send_message(user_id, "Промокод полностью активирован")
        else:
            await bot.send_message(user_id, "Промокод не найден")
    else:
        await bot.send_message(user_id, "Пожалуйста, введите промокод для активации /activate `promocode`")

@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().split()
    if user_id == int(ADMIN_ID):
        if len(args) >= 4: 
            promocode_id = args[0]
            balance = args[1]
            count = args[3]
            coins = args[2]
            description = ' '.join(args[4:])  
            if db.promocode_exists(promocode_id):
                await bot.send_message(user_id, "Промокод уже существует")
            else:
                if not balance.isdigit() or not count.isdigit() or int(balance) <= 0 or int(count) <= 0:
                    await bot.send_message(user_id, "Сумма и количество должны быть положительными числами больше нуля")
                else:
                    db.add_promocode(promocode_id, balance, coins, count, description)
                    await bot.send_message(user_id, f"Промокод успешно создан.\nНазвание: <code>{promocode_id}</code>\nСумма: <b>{balance} {coins}</b>\nКоличество: <b>{count}</b>\nОписание: <b>{description}</b>\n\n<b>Ссылочка для активации</b>: <a href=\"https://t.me/{USERNAME_BOT}?start={promocode_id}\">Нажми!</a>", reply_markup=admin_menu, parse_mode=ParseMode.HTML)
        else:
            await bot.send_message(user_id, "Пожалуйста, введите данные для создания промокода /create `promocode` `balance` `coin_type` `count` `description`")
    else:
        pass


@dp.message_handler(commands=['info', 'help'])
async def info(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id == int(ADMIN_ID):
        await bot.send_message(user_id, info_commands_admin, reply_markup=admin_menu, parse_mode=ParseMode.HTML)
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
                await bot.send_message(user_id, "Промокод успешно деактивирован", reply_markup=admin_menu)
            else:
                await bot.send_message(user_id, "Промокод не найден")
        else:
            await bot.send_message(user_id, "Пожалуйста, введите промокод для удаления /deactivate `promocode`")
    else:
        pass

@dp.callback_query_handler(lambda query: query.data == 'statsbtn')
async def stats(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    if user_id == int(ADMIN_ID):
        active_promocodes = db.get_active_promocodes()
        if active_promocodes:
            formatted_promocodes = "\n".join([f"ID: {promocode[0]}, Название: {promocode[1]}, Сумма: {promocode[2]} {promocode[4]}, Кол-во активаций: {promocode[3]}, Описание: {promocode[5]}" for promocode in active_promocodes])
            await bot.send_message(user_id, f"Активные промокоды:\n{formatted_promocodes}", reply_markup=admin_menu)
        else:
            await bot.send_message(user_id, "Нет активных промокодов", reply_markup=admin_menu)
    else:
        pass

@dp.callback_query_handler(lambda query: query.data == 'infobtn')
async def info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    if user_id == int(ADMIN_ID):
        await bot.send_message(user_id, info_commands_admin, reply_markup=admin_menu, parse_mode=ParseMode.HTML)
    else:
        pass

# @dp.inline_handler()
# async def inline_handler(inline_query: types.InlineQuery):
#     user_id = inline_query.from_user.id
#     if user_id == int(ADMIN_ID):
#         active_promocodes = db.get_active_promocodes()
#         results = [
#             types.InlineQueryResultArticle(
#                 id='1',
#                 title='Статистика',
#                 input_message_content=types.InputTextMessageContent(f"Активные промокоды: {active_promocodes}"),
#                 description='Статистика активных промокодов',
#                 thumb_url='https://cdn4.iconfinder.com/data/icons/flat-brand-logo-2/512/telegram-512.png',
#             ),
#             types.InlineQueryResultArticle(
#                 id='2',
#                 title='Информация',
#                 input_message_content=types.InputTextMessageContent(info_commands_admin, parse_mode=ParseMode.HTML),
#                 description='Информация о командах',
#                 thumb_url='https://cdn4.iconfinder.com/data/icons/flat-brand-logo-2/512/telegram-512.png',
#             ),
#         ]
#         await bot.answer_inline_query(inline_query.id, results, cache_time=1)
#     else:
#         pass

@dp.inline_handler()
async def promocode_inline(inline_query: types.InlineQuery):
    results = []

    # Получаем список активных промокодов из базы данных
    promocodes = db.get_all_promocodes()
    user_id = inline_query.from_user.id
    if user_id == int(ADMIN_ID):

        for promocode in promocodes:
            title = promocode[1]
            balance = promocode[2]
            description = promocode[5]
            activation_count = promocode[3]
            coins = promocode[4]

            # Формируем текст сообщения для каждого промокода
            message_text = (
                f"<b>Промокод</b>\n"
                f"<b>Название промокода</b>: <code>{title}</code>\n"
                f"<b>Описание</b>: {description}\n"
                f"<b>Кол-во активаций</b>: <code>{activation_count}</code>\n"
                f"<b>Сумма 1 активации</b>: <code>{balance} {coins}</code>\n"
                f"<b>Ссылка</b>: <a href=\"https://t.me/{USERNAME_BOT}?start={title}\">Нажми!</a>"
            )

            # Создаем объект InlineQueryResultArticle для каждого промокода
            result = types.InlineQueryResultArticle(
                id=str(promocode[0]),
                title=title,
                description=description,
                input_message_content=types.InputTextMessageContent(message_text, parse_mode=ParseMode.HTML)
            )

            results.append(result)
        
        await bot.answer_inline_query(inline_query.id, results, cache_time=1)
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
