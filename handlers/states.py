from aiogram.dispatcher.filters.state import StatesGroup, State

from typing import Dict, List


class ProductsState(StatesGroup):

    next_page_number: str = State()
    user_id: int = State()
    message_to_product_id: Dict[int, str] = State()


class CategoriesState(StatesGroup):

    categories: List[Dict] = State()
    categories_slug_list: List[str] = State()
    message_to_product_id: Dict[int, str] = State()
