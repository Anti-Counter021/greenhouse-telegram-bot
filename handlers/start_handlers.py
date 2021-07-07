from aiogram import types

from dispatcher import dispatcher
from server_requests import HOST


@dispatcher.message_handler(commands=['link'])
async def link(message: types.Message):
    await message.answer(f'Ссылка на наш сайт {HOST}')


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f'Приветствую @{message.from_user.username}!\n'
        f'Я бот от сайта по продже теплиц. Вы можете получить ссылку на наш сайт командой /link.\n'
        f'У меня ограниченный функционал, поэтому рекомендую всё-таки использовать наш сайт.'
    )
