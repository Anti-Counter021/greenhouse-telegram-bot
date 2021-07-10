from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher
from states import LoginState, RegisterState, ResetPasswordState, MakeOrderState, ReviewState
from server_requests import request_login, profile_request, logout_request, request_register, request_reset_password


@dispatcher.message_handler(commands=['reset_password'])
async def reset_password(message: types.Message):

    await message.answer('Пожалуйста введите почту для отправки сообщения о сбросе пароля')

    dispatcher.register_message_handler(reset_password_email_set, state=ResetPasswordState.email)

    await ResetPasswordState.email.set()


async def reset_password_email_set(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        try:
            request_reset_password.reset_password(message.text)
            data['email'] = message.text
            await message.answer('Письмо отправлено!')
            dispatcher.message_handlers.unregister(reset_password_email_set)
            await state.finish()
        except:
            await message.answer('Такой почты не существует! Введите другую')
            return


@dispatcher.message_handler(commands=['register'])
async def register(message: types.Message):

    await message.answer('Пожалуйста введите желаемое имя пользователя')

    dispatcher.register_message_handler(set_username_register, state=RegisterState.username)
    dispatcher.register_message_handler(set_first_name_register, state=RegisterState.first_name)
    dispatcher.register_message_handler(set_last_name_register, state=RegisterState.last_name)
    dispatcher.register_message_handler(set_email_register, state=RegisterState.email)
    dispatcher.register_message_handler(set_phone_register, state=RegisterState.phone)
    dispatcher.register_message_handler(set_address_register, state=RegisterState.address)
    dispatcher.register_message_handler(set_password_register, state=RegisterState.password)

    await RegisterState.username.set()


async def set_username_register(message: types.Message, state: FSMContext):

    async with state.proxy() as data:

        try:
            request_register.exists_username(message.text)
            await message.answer('Такое имя пользователя уже существует. Пожалуйства введите другое.')
            return
        except:
            data['username'] = message.text

            await message.answer('Пожалуйста введите ваше имя')
            await RegisterState.first_name.set()


async def set_first_name_register(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['first_name'] = message.text

        await message.answer('Пожалуйста введите вашу фамилию')
        await RegisterState.last_name.set()


async def set_last_name_register(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['last_name'] = message.text

        await message.answer('Пожалуйста введите вашу почту')
        await RegisterState.email.set()


async def set_email_register(message: types.Message, state: FSMContext):

    if ('@' not in message.text) or ('.' not in message.text):
        await message.answer('Пожалуйста введите корректную почту!')
        return

    async with state.proxy() as data:
        try:
            request_register.exists_email(message.text)
            await message.answer('Такое почта уже существует. Пожалуйства введите другую.')
            return
        except:
            data['email'] = message.text

            await message.answer('Пожалуйста введите ваш номер телефона')
            await RegisterState.phone.set()


async def set_phone_register(message: types.Message, state: FSMContext):

    if len(message.text) > 30:
        await message.answer('Телефон не может быть длиннее 30 символов!')
        return

    async with state.proxy() as data:
        data['phone'] = message.text

        await message.answer('Пожалуйста введите ваш адрес')
        await RegisterState.address.set()


async def set_address_register(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['address'] = message.text

        await message.answer('Пожалуйста введите пароль в таком виде:')
        await message.answer('пароль_повторить пароль')
        await RegisterState.password.set()


async def set_password_register(message: types.Message, state: FSMContext):

    password, password_confirm = message.text.split('_')

    if password_confirm != password:
        await message.answer('Пароли не совпадают!')
        return

    if len(password) <= 8:
        await message.answer('Пароль должен быть больше 8 символов в длину!')
        return

    async with state.proxy() as data:
        data['password'] = password
        data['confirm_password'] = password_confirm

        request_register.register({**data})
        await message.answer('Вы зарегистрированы успешно! Введите комманду /login чтобы авторизироваться')

    dispatcher.message_handlers.unregister(set_username_register)
    dispatcher.message_handlers.unregister(set_first_name_register)
    dispatcher.message_handlers.unregister(set_last_name_register)
    dispatcher.message_handlers.unregister(set_email_register)
    dispatcher.message_handlers.unregister(set_phone_register)
    dispatcher.message_handlers.unregister(set_address_register)
    dispatcher.message_handlers.unregister(set_password_register)

    await state.finish()


@dispatcher.message_handler(commands=['login'])
async def login(message: types.Message):

    await message.answer('Пожалуйста введите своё имя пользователя')
    dispatcher.register_message_handler(set_username_login, state=LoginState.username)
    dispatcher.register_message_handler(set_password_login, state=LoginState.password)
    await LoginState.username.set()


async def set_username_login(message: types.Message, state: FSMContext):

    async with state.proxy() as data:

        try:
            request_login.exists_username(message.text)
            data['username'] = message.text

            await message.answer('Пожалуйста введите пароль')
            await LoginState.password.set()
        except:
            await message.answer('Такого пользователя не существует. Попробуйте пожалуйста ещё раз')


async def set_password_login(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['password'] = message.text

        try:
            data['token'] = request_login.login({'username': data['username'], 'password': data['password']})['token']
        except:
            await message.answer('Пожалуйста попробуйте ввести другой пароль')
            return

        await message.answer(f'Вот ваш токен {data["token"]}')
    dispatcher.message_handlers.unregister(set_username_login)
    dispatcher.message_handlers.unregister(set_password_login)


@dispatcher.message_handler(state=[LoginState, MakeOrderState, ReviewState], commands=['profile'])
async def get_profile(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        await message.answer('Ваши заказы:')
        for order in profile_request(data['token']).load_json():
            await message.answer('======================================================')
            for cart_product in order['cart']['products']:
                await message.answer(
                    f'{cart_product["product"]["title"]} в количестве {cart_product["qty"]} шт.\n'
                    f'Цена: {cart_product["price"]} руб.\n'
                    f'Общая цена: {cart_product["final_price"]} руб.\n'
                )
            await message.answer(f'Итого {order["cart"]["final_price"]} руб.')


@dispatcher.message_handler(state=[LoginState, MakeOrderState, ReviewState], commands=['logout'])
async def logout(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        logout_request(data['token']).load_json()

    await state.finish()
    await message.answer('Вы вышли из сети!')
