from aiogram import types

from typing import List, Dict

from dispatcher import dispatcher, bot
from server_requests.categories import request_categories
from utils import load_products

categories: List[Dict] = []
categories_slug_list: List[str] = []


@dispatcher.message_handler(commands=['categories'])
async def get_categories(message: types.Message):
    global categories, categories_slug_list

    categories = request_categories.load_json()
    categories_btn_list: List[types.InlineKeyboardButton] = []
    for category in categories:
        categories_slug_list.append(category['slug'])
        categories_btn_list.append(types.InlineKeyboardButton(category['name'], callback_data=category['slug']))
    categories_keyboard = types.InlineKeyboardMarkup().row(*categories_btn_list)
    await message.answer('Наши категории', reply_markup=categories_keyboard)


@dispatcher.callback_query_handler(lambda data: data.data in categories_slug_list)
async def callback_categories(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    category_select = list(filter(lambda c: c['slug'] == callback_query.data, categories))[0]
    await bot.send_message(
        callback_query.from_user.id,
        f'Выбрана категория - <strong>{category_select["name"]}</strong>\n'
        f'Товары к этой категории:'
    )
    await load_products(category_select['products'], callback_query.from_user.id)
