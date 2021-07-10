from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher
from states import MakeOrderState, LoginState, ReviewState
from server_requests import request_review
from utils import parse_reviews


@dispatcher.message_handler(commands=['reviews'], state=[None, MakeOrderState, LoginState, ReviewState])
async def get_reviews(message: types.Message, state: FSMContext):

    await message.answer('Вот первые несколько отзывов по вашему запросу:')

    response = request_review().reviews()
    await parse_reviews(response, message, state)
