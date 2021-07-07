from aiogram.dispatcher.filters.state import StatesGroup, State

from typing import Dict


class ProductsState(StatesGroup):

    next_page_number: str = State()
    user_id: int = State()
    message_to_product_id: Dict[int, str] = State()
