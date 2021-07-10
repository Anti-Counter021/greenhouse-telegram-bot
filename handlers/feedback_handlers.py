from aiogram import types

from dispatcher import dispatcher
from states import LoginState, MakeOrderState
from server_requests import request_feedback


@dispatcher.message_handler(commands=['feedback'], state=[None, LoginState, MakeOrderState])
async def feedback(message: types.Message):

    dispatcher.register_message_handler(text, state=[None, LoginState, MakeOrderState])
    await message.answer('Введите сообщение для отправки')


async def text(message: types.Message):

    request_feedback.post_json({'text': message.text})
    await message.answer('Ваше сообщение отправлено')

    dispatcher.message_handlers.unregister(text)
