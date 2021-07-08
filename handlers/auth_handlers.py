from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher
from states import LoginState
from server_requests import request_login, profile_request


@dispatcher.message_handler(commands=['login'])
async def login(message: types.Message):

    await message.answer('Пожалуйста введите своё имя пользователя')
    dispatcher.register_message_handler(set_username, state=LoginState.username)
    dispatcher.register_message_handler(set_password, state=LoginState.password)
    await LoginState.username.set()


async def set_username(message: types.Message, state: FSMContext):

    async with state.proxy() as data:

        try:
            request_login.exists_username({'username': message.text})
            data['username'] = message.text

            await message.answer('Пожалуйста введите пароль')
            await LoginState.password.set()
        except:
            await message.answer('Такого пользователя не существует. Попробуйте пожалуйста ещё раз')


async def set_password(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['password'] = message.text

        try:
            data['token'] = request_login.login({'username': data['username'], 'password': data['password']})['token']
        except:
            await message.answer('Пожалуйста попробуйте ввести другой пароль')
            return

        await message.answer(f'Вот ваш токен {data["token"]}')
    dispatcher.message_handlers.unregister(set_username)
    dispatcher.message_handlers.unregister(set_password)


@dispatcher.message_handler(state=LoginState, commands=['profile'])
async def get_profile(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        await message.answer(profile_request(data['token']).load_json())
