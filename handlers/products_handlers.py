from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher, bot
from .state import ProductsState
from server_requests import request_products
from utils import load_products, product_detail_load


async def parse_product(response: dict, state: FSMContext = ProductsState):

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


@dispatcher.message_handler(commands=['products'])
async def get_products(message: types.Message, state: FSMContext):

    await message.answer('Вот первые несколько товаров по вашему запросу:')
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
    response = request_products.products()
    await parse_product(response, state)


@dispatcher.message_handler(commands=['detail'], state=ProductsState)
async def detail_product(message: types.Message, state: FSMContext):

    if not message.reply_to_message:
        await message.reply('Это сообщение должно быть ответом на тот товар, который вы хотите детально посмотреть!')
        return

    async with state.proxy() as data:
        if message.reply_to_message.message_id not in data['message_to_product_id'].keys():
            await message.reply('Выберите пожалуйста сообщение с товаром!')
            return

        slug = data['message_to_product_id'][message.reply_to_message.message_id]

        response = request_products.detail_product(slug)

        await product_detail_load(response, message.from_user.id)


@dispatcher.callback_query_handler()
async def callback_products(callback_query: types.CallbackQuery, state: FSMContext = ProductsState):

    async with state.proxy() as data:
        if not callback_query.data == data['next_page_number']:
            return

    await bot.answer_callback_query(callback_query.id)

    await callback_query.answer('Вот ещё товары по вашему запросу:')
    response = request_products.products(callback_query.data)
    await parse_product(response, state)

    await bot.edit_message_reply_markup(
        callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None
    )
