from aiogram import types
from aiogram.dispatcher import FSMContext

from dispatcher import dispatcher, bot
from states import LoginState, MakeOrderState, ReviewState
from server_requests import request_products, request_review
from utils import load_products, parse_product, parse_reviews


@dispatcher.callback_query_handler(state=[None, MakeOrderState, LoginState, ReviewState])
async def callback_categories(callback_query: types.CallbackQuery, state: FSMContext):

    await bot.answer_callback_query(callback_query.id)

    async with state.proxy() as data:

        if 'categories_slug_list' in data.keys() and callback_query.data in data['categories_slug_list']:

            category_select = list(filter(lambda c: c['slug'] == callback_query.data, data['categories']))[0]
            await bot.send_message(
                callback_query.from_user.id,
                f'Выбрана категория - <strong>{category_select["name"]}</strong>\n'
                f'Товары к этой категории:'
            )
            data['message_to_product_id'] = await load_products(
                category_select['products'], callback_query.from_user.id
            )
            return

        if 'next_page_number' in data.keys() and callback_query.data == data['next_page_number']:

            await callback_query.answer('Вот ещё товары по вашему запросу:')
            response = request_products.products(callback_query.data)
            await parse_product(response, state)

            await bot.edit_message_reply_markup(
                callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None
            )
            return

        if 'next_page_number_reviews' in data.keys() and \
                callback_query.data == data['next_page_number_reviews']:

            await callback_query.answer('Вот ещё отзывы по вашему запросу:')
            response = request_review().reviews(callback_query.data.replace('review/', ''))

            await parse_reviews(response, callback_query.message, state)

            await bot.edit_message_reply_markup(
                callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None
            )
            return
