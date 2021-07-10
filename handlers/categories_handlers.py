from aiogram import types
from aiogram.dispatcher import FSMContext

from typing import List

from dispatcher import dispatcher
from states import LoginState, MakeOrderState, ReviewState
from server_requests import request_categories


@dispatcher.message_handler(commands=['categories'], state=[None, LoginState, MakeOrderState, ReviewState])
async def get_categories(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data['categories'] = request_categories.load_json()
        data['categories_slug_list'] = []
        categories_btn_list: List[types.InlineKeyboardButton] = []
        for category in data['categories']:
            data['categories_slug_list'].append(category['slug'])
            categories_btn_list.append(types.InlineKeyboardButton(category['name'], callback_data=category['slug']))
        categories_keyboard = types.InlineKeyboardMarkup().row(*categories_btn_list)
        await message.answer('Наши категории', reply_markup=categories_keyboard)
