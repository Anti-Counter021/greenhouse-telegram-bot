from aiogram import types
from aiogram.dispatcher import FSMContext

from datetime import datetime

from dispatcher import dispatcher
from states import LoginState, MakeOrderState
from server_requests import request_order, request_cart


@dispatcher.message_handler(commands=['make'], state=[LoginState, MakeOrderState])
async def make_order(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        if not request_cart(data['token']).cart()['products']:
            await message.answer('У вас пустая корзина!')
            return

    await message.answer('Оформление заказа. Пожалуйста вводите правдивые данные, чтобы мы могли с вами связаться')

    dispatcher.register_message_handler(set_first_name_make, state=MakeOrderState.first_name)
    dispatcher.register_message_handler(set_last_name_make, state=MakeOrderState.last_name)
    dispatcher.register_message_handler(set_phone_make, state=MakeOrderState.phone)
    dispatcher.register_message_handler(set_address_make, state=MakeOrderState.address)
    dispatcher.register_message_handler(set_buying_type_make, state=MakeOrderState.buying_type)
    dispatcher.register_message_handler(set_order_date_make, state=MakeOrderState.order_date)

    await message.answer('Введите что-нибудь для продолжения')

    await MakeOrderState.first_name.set()


async def set_first_name_make(message: types.Message, state: FSMContext):

    await message.answer('Введите своё имя')

    async with state.proxy() as data:
        data['first_name'] = message.text
        await MakeOrderState.last_name.set()


async def set_last_name_make(message: types.Message, state: FSMContext):

    await message.answer('Введите свою фамилию')

    async with state.proxy() as data:
        data['last_name'] = message.text
        await MakeOrderState.phone.set()


async def set_phone_make(message: types.Message, state: FSMContext):

    await message.answer('Введите свой номер телефона')

    async with state.proxy() as data:
        data['phone'] = message.text
        await MakeOrderState.address.set()


async def set_address_make(message: types.Message, state: FSMContext):

    await message.answer('Введите адрес доставки товара')

    async with state.proxy() as data:
        data['address'] = message.text
        await MakeOrderState.buying_type.set()


async def set_buying_type_make(message: types.Message, state: FSMContext):

    self = types.KeyboardButton('Самовывоз')
    delivery = types.KeyboardButton('Доставка')
    buying_type_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row(self, delivery)

    await message.answer('Выберите тип заказа', reply_markup=buying_type_keyboard)

    async with state.proxy() as data:

        if message.text not in ('Самовывоз', 'Доставка'):
            await message.answer('Выберите тип заказа нажатием на одну из кнопок!')
            return

        await message.answer(
            f'Введите желаемую дату получения в формате: "дд/мм/гггг"', reply_markup=types.ReplyKeyboardRemove()
        )
        data['buying_type'] = message.text
        await MakeOrderState.order_date.set()


async def set_order_date_make(message: types.Message, state: FSMContext):

    try:
        if datetime.strptime(message.text, '%d/%m/%Y').date() < datetime.today().date():
            await message.answer('Желаемая дата получения не может быть прошедшей!')
            return

        if datetime.strptime(message.text, '%d/%m/%Y').year > datetime.utcnow().year + 1:
            await message.answer('Дата слишком большая!')
            return

    except ValueError:
        await message.answer('Введите дату в нужном формате!')
        return

    async with state.proxy() as data:
        data['order_date'] = message.text

        request_order(data['token']).post_json({**data})

        dispatcher.message_handlers.unregister(set_first_name_make)
        dispatcher.message_handlers.unregister(set_last_name_make)
        dispatcher.message_handlers.unregister(set_phone_make)
        dispatcher.message_handlers.unregister(set_address_make)
        dispatcher.message_handlers.unregister(set_buying_type_make)
        dispatcher.message_handlers.unregister(set_order_date_make)

        await message.answer(
            'Заказ создан успешно. Ждите ответа!'
        )
