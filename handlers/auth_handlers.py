from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher
from states import LoginState
from server_requests import request_login


# @dispatcher.message_handler(commands=['token'], state=LoginState)
# async def get_token(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         await message.answer(f'Токен: {data["token"]}')


@dispatcher.message_handler(commands=['login'])
async def login(message: types.Message):

    await message.answer('Пожалуйста введите своё имя пользователя')
    await LoginState.username.set()


@dispatcher.message_handler(state=LoginState.username)
async def set_username(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['username'] = message.text

    await message.answer('Пожалуйста введите пароль')
    await LoginState.password.set()


@dispatcher.message_handler(state=LoginState.password)
async def set_password(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['password'] = message.text
        data['token'] = request_login.post_json({**data})
        await message.answer(f'Вот ваш токен {data["token"]}')
