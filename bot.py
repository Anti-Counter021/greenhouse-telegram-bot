from aiogram import Bot, Dispatcher, executor, types

import logging

from typing import List

from config import TOKEN
from server_requests import request_products, request_categories, HOST

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot=bot)

categories = []
categories_slug_list: List[str] = []


@dispatcher.message_handler(commands=['categories'])
async def get_categories(message: types.Message):
    global categories, categories_slug_list

    categories = request_categories.load_json()
    categories_btn_list: List[types.InlineKeyboardButton] = []
    for category in categories:
        categories_slug_list.append('category/' + category['slug'])
        categories_btn_list.append(types.InlineKeyboardButton(category['name'], callback_data=category['slug']))
    categories_keyboard = types.InlineKeyboardMarkup().row(*categories_btn_list)
    await message.answer('Наши категории', reply_markup=categories_keyboard)


@dispatcher.message_handler(commands=['products'])
async def get_products(message: types.Message):
    await message.answer(request_products.products())


@dispatcher.callback_query_handler(lambda data: data.data)
async def callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    if f'category/{callback_query.data}' in (categories_slug_list):
        category_select = list(filter(lambda c: c['slug'] == callback_query.data, categories))[0]
        await bot.send_message(
            callback_query.from_user.id,
            f'Выбрана категория - <strong>{category_select["name"]}</strong>\n'
            f'Товары к этой категории:'
        )
        for product in category_select['products']:
            price = f'{product["price"]} руб.' if not product["discount"] else \
                f'<del>{product["price"]}</del> <strong>-{product["discount"]}%</strong>\n' \
                f'{product["price_with_discount"]} руб.'
            await bot.send_message(
                callback_query.from_user.id,
                f'{product["title"]}\n'
                f'{price}\n'
                f'{product["description"]}'
            )
            await bot.send_message(callback_query.from_user.id, HOST + "/products/" + product["slug"])
    # await bot.edit_message_reply_markup(
    #     callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None
    # )


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
