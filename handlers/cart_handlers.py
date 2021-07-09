from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher
from states import LoginState
from server_requests import request_cart


@dispatcher.message_handler(commands=['cart'], state=LoginState)
async def get_cart(message: types.Message, state: FSMContext):

    async with state.proxy() as data:

        cart = request_cart(data['token']).cart()
        await message.answer('Ваша корзина')

        for cart_product in cart['products']:
            await message.answer(f'{cart_product["product"]["title"]} в количестве {cart_product["qty"]} шт.')
            await message.answer(f'Цена: {cart_product["price"]} руб.\nОбщая цена: {cart_product["final_price"]} руб.')
        await message.answer(f'Итого: {cart["final_price"]} руб.')


@dispatcher.message_handler(commands=['add'], state=LoginState)
async def add_to_cart(message: types.Message, state: FSMContext):

    if not message.reply_to_message:
        await message.reply('Это сообщение должно быть ответом на тот товар, который вы хотите добавить в корзину!')
        return

    async with state.proxy() as data:
        if 'token' not in data.keys():
            await message.answer('Вы не авторизированы!')
            return

        if 'message_to_product_id' not in data.keys():
            await message.reply('Выберите пожалуйста сообщение с товаром!')
            return

        if message.reply_to_message.message_id not in data['message_to_product_id'].keys():
            await message.reply('Выберите пожалуйста сообщение с товаром!')
            return

        product_id = data['message_to_product_id'][message.reply_to_message.message_id]['id']
        try:
            request_cart(data['token']).add_to_cart(product_id)
            await message.answer('Товар добавлен в корзину!')
        except:
            await message.answer('Этот товар уже в корзине!')
