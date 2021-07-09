from aiogram import types
from aiogram.dispatcher import FSMContext

from typing import Dict

from dispatcher import dispatcher
from states import LoginState
from server_requests import request_cart


async def check_message(data, message: types.Message):
    
    if 'token' not in data.keys():
        await message.answer('Вы не авторизованы!')
        return

    if 'message_to_product_id' not in data.keys() or \
            message.reply_to_message.message_id not in data['message_to_product_id'].keys():
        await message.reply('Выберите пожалуйста сообщение с товаром!')
        return

    return True


@dispatcher.message_handler(commands=['cart'], state=LoginState)
async def get_cart(message: types.Message, state: FSMContext):

    async with state.proxy() as data:

        data['message_to_product_id']: Dict[int, Dict[str]] = {}

        cart = request_cart(data['token']).cart()
        await message.answer('Ваша корзина')

        for cart_product in cart['products']:
            message_id = await message.answer(
                f'{cart_product["product"]["title"]} в количестве {cart_product["qty"]} шт.\n'
                f'Цена: {cart_product["price"]} руб.\nОбщая цена: {cart_product["final_price"]} руб.'
            )
            data['message_to_product_id'][message_id["message_id"]] = {
                'id': cart_product['id']
            }
        await message.answer(f'Итого: {cart["final_price"]} руб.')
        await message.answer(
            'Если хотите добавить ещё товары. То вам нужно их повторно запросить при помощи /products или /categories'
        )


@dispatcher.message_handler(commands=['add'], state=LoginState)
async def add_to_cart(message: types.Message, state: FSMContext):

    if not message.reply_to_message:
        await message.reply('Это сообщение должно быть ответом на тот товар, который вы хотите добавить в корзину!')
        return

    async with state.proxy() as data:

        if not await check_message(data, message):
            return

        if message.reply_to_message.message_id not in data['message_to_product_id'].keys() or \
                'slug' not in data['message_to_product_id'][message.reply_to_message.message_id].keys():
            await message.answer('Выберите нормальный товар!')
            return

        product_id = data['message_to_product_id'][message.reply_to_message.message_id]['id']
        try:
            request_cart(data['token']).add_to_cart(product_id)
            await message.answer('Товар добавлен в корзину!')
            await get_cart(message, state)
        except:
            await message.answer('Этот товар уже в корзине!')


@dispatcher.message_handler(commands=['remove'], state=LoginState)
async def remove_from_cart(message: types.Message, state: FSMContext):

    if not message.reply_to_message:
        await message.reply('Это сообщение должно быть ответом на тот товар, который вы хотите удалить из корзины!')
        return

    async with state.proxy() as data:

        if not await check_message(data, message):
            return

        if 'slug' in data['message_to_product_id'][message.reply_to_message.message_id].keys():
            await message.answer('Выберите товар из корзины!')
            return

        cart_product_id = data['message_to_product_id'][message.reply_to_message.message_id]['id']
        try:
            request_cart(data['token']).remove_product_from_cart(cart_product_id)
            await message.answer('Товар был удалён')
            await get_cart(message, state)
        except:
            await message.answer('Обновите корзину и выберите от туда товар для удаления!')


@dispatcher.message_handler(commands=['change'], state=LoginState)
async def change_qty(message: types.Message, state: FSMContext):

    if not message.reply_to_message:
        await message.reply(
            'Это сообщение должно быть ответом на тот товар, количество которого вы хотите изменить в корзине!'
        )
        return

    if not message.get_args():
        await message.answer(
            'Чтобы изменить количество необходимо после команды написать число,'
            ' на которое вы хотите изменить количество товара'
        )
        return

    try:
        if int(message.get_args()) < 1:
            await message.answer('Количество товара не может быть меньше 1!')
            return
    except ValueError:
        await message.answer('Количество товара может быть только числом!')
        return

    async with state.proxy() as data:

        if not await check_message(data, message):
            return

        if 'slug' in data['message_to_product_id'][message.reply_to_message.message_id].keys():
            await message.answer('Выберите товар из корзины!')
            return

        cart_product_id = data['message_to_product_id'][message.reply_to_message.message_id]['id']
        try:
            request_cart(data['token']).change_qry(cart_product_id, message.get_args())
            await message.answer(f'Количество товара изменено на {message.get_args()}')
            await get_cart(message, state)
        except:
            await message.answer('Обновите корзину и выберите от туда товар для изменения его количества!')
