from aiogram import types

from dispatcher import dispatcher, bot
from server_requests import request_products
from utils import load_products

next_page_number: str = ''
user_id: int = 0


async def parse_product(response: dict):
    global next_page_number

    await load_products(response['results'], user_id)
    if response['next']:
        next_page_number = response['next'].split('=')[-1]
        next_load_btn = types.InlineKeyboardButton(
            'Загрузить ещё', callback_data=next_page_number,
        )
        next_load_keyboard = types.InlineKeyboardMarkup().row(next_load_btn)
        await bot.send_message(user_id, 'Можете загрузить ещё', reply_markup=next_load_keyboard)
    else:
        await bot.send_message(user_id, f'Это все наши товары. Всего их {response["count"]} штук')


@dispatcher.message_handler(commands=['products'])
async def get_products(message: types.Message):
    global user_id

    await message.answer('Вот первые несколько товаров по вашему запросу:')
    user_id = message.from_user.id
    response = request_products.products()
    await parse_product(response)


@dispatcher.callback_query_handler(lambda data: data.data == next_page_number)
async def callback_products(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.answer('Вот ещё товары по вашему запросу:')
    response = request_products.products(callback_query.data)
    await parse_product(response)

    await bot.edit_message_reply_markup(
        callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None
    )
