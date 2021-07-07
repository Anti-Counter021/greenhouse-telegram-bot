from aiogram import Bot, Dispatcher, types

import logging

from config import TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dispatcher = Dispatcher(bot=bot)
