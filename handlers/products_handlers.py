from aiogram import types

from dispatcher import dispatcher
from server_requests import request_products


@dispatcher.message_handler(commands=['products'])
async def get_products(message: types.Message):
    await message.answer(request_products.products())
