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


class RegisterState(StatesGroup):

    username: str = State()
    email: str = State()
    first_name: str = State()
    last_name: str = State()
    phone: str = State()
    address: str = State()
    password: str = State()
    confirm_password: str = State()


class LoginState(StatesGroup):

    username: str = State()
    password: str = State()
    token: str = State()
