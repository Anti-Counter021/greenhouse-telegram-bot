from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher
from states import LoginState
from server_requests import request_products
from utils import product_detail_load, parse_product, product_features


@dispatcher.message_handler(commands=['products'], state=[None, LoginState])
async def get_products(message: types.Message, state: FSMContext):

    await message.answer('Вот первые несколько товаров по вашему запросу:')
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
    response = request_products.products()
    await parse_product(response, state)


@dispatcher.message_handler(commands=['detail'], state=[None, LoginState])
async def detail_product(message: types.Message, state: FSMContext):

    if not message.reply_to_message:
        await message.reply('Это сообщение должно быть ответом на тот товар, который вы хотите детально посмотреть!')
        return

    async with state.proxy() as data:
        if 'message_to_product_id' not in data.keys() or message.reply_to_message.message_id not in data['message_to_product_id'].keys():
            await message.reply('Выберите пожалуйста сообщение с товаром!')
            return

        slug = data['message_to_product_id'][message.reply_to_message.message_id]['slug']

        response = request_products.detail_product(slug)

        await product_detail_load(response, message.from_user.id)
        if response['features']:
            await product_features(response['features'], message.from_user.id)
