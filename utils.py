from aiogram import types
from aiogram.dispatcher import FSMContext

from datetime import datetime

from typing import Dict, List

from dispatcher import bot
from server_requests import HOST


async def product_features(features: List[Dict], user_id: int) -> None:

    features_str = 'Название - Характеристика\n'

    for feature in features:
        features_str += \
            f'\n\t\t{feature["name"]} - {feature["feature_value"]}{feature["unit"] if feature["unit"] else ""}'

    await bot.send_message(
        user_id,
        features_str
    )


async def product_detail_load(product: Dict, user_id: int) -> int:

    price = f'{product["price"]} руб.' if not product["discount"] else \
        f'<del>{product["price"]}</del> <strong>-{product["discount"]}%</strong>\n' \
        f'{product["price_with_discount"]} руб.'

    message = await bot.send_message(
        user_id,
        f'{product["title"]}\n'
        f'{price}\n'
        f'{product["description"]}'
    )

    await bot.send_message(user_id, HOST + "/products/" + product["slug"])
    return message.message_id


async def load_products(products: List[Dict], user_id: int):
    message_to_product_id: Dict[int, Dict[str]] = {}

    for product in products:
        message_id = await product_detail_load(product, user_id)
        message_to_product_id[message_id] = {'slug': product['slug'], 'id': product['id']}

    return message_to_product_id


async def parse_product(response: dict, state: FSMContext):

    async with state.proxy() as data:

        message_to_product_response = await load_products(response['results'], data['user_id'])
        if response['next']:
            data['next_page_number'] = response['next'].split('=')[-1]
            next_load_btn = types.InlineKeyboardButton(
                'Загрузить ещё', callback_data=data['next_page_number'],
            )
            next_load_keyboard = types.InlineKeyboardMarkup().row(next_load_btn)
            await bot.send_message(data['user_id'], 'Можете загрузить ещё', reply_markup=next_load_keyboard)
        else:
            await bot.send_message(data['user_id'], f'Это все наши товары. Всего их {response["count"]} штук')
        if 'message_to_product_id' not in data.keys():
            data['message_to_product_id'] = {**message_to_product_response}
        else:
            data['message_to_product_id'] = {**data['message_to_product_id'], **message_to_product_response}


async def review_load(review: Dict, message: types.Message):

    await message.answer(f'Автор отзыва - {review["user"]}')
    await message.answer(
        f'{review["comment"]} Дата публикации '
        f'{datetime.fromisoformat(review["created_at"][:-1]).strftime("%d/%m/%Y")}'
    )


async def parse_reviews(response: dict, message: types.message, state: FSMContext):

    async with state.proxy() as data:

        for review in response['results']:
            await review_load(review, message)

        if response['next']:
            data['next_page_number_reviews'] = f"review/{response['next'].split('=')[-1]}"
            next_load_btn = types.InlineKeyboardButton(
                'Загрузить ещё', callback_data=data['next_page_number_reviews'],
            )
            next_load_keyboard = types.InlineKeyboardMarkup().row(next_load_btn)
            await message.answer('Можете загрузить ещё', reply_markup=next_load_keyboard)
        else:
            await message.answer(f'Это все наши отзывы. Всего их {response["count"]} штук')
