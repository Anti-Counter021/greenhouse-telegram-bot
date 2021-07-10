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


@dispatcher.message_handler(commands=['new_review'], state=[LoginState, MakeOrderState, ReviewState])
async def create_review(message: types.Message):

    await message.answer('Создание отзыва')

    await message.answer('Введите оценку, которую вы поставите сайту:')

    dispatcher.register_message_handler(set_appraisal_review, state=ReviewState.appraisal)
    dispatcher.register_message_handler(set_comment_review, state=ReviewState.comment)

    await ReviewState.appraisal.set()


async def set_appraisal_review(message: types.Message, state: FSMContext):

    try:
        appraisal = int(message.text)
        if not 0 < appraisal < 6:
            await message.answer('Оценка должна быть не ниже 1 и не выше 5!')
            return
    except ValueError:
        await message.answer('Введите пожалуйста число!')
        return

    async with state.proxy() as data:
        data['appraisal'] = message.text

        await message.answer('Введите комментарий к отзыву')

        await ReviewState.comment.set()


async def set_comment_review(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['comment'] = message.text

        request_review(data['token']).post_json({**data})

        dispatcher.message_handlers.unregister(set_appraisal_review)
        dispatcher.message_handlers.unregister(set_comment_review)

        await message.answer('Отзыв был создан успешно!')
