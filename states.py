from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductsState(StatesGroup):

    next_page_number = State()
    user_id = State()
    message_to_product_id = State()


class CategoriesState(StatesGroup):

    categories = State()
    categories_slug_list = State()
    message_to_product_id = State()


class RegisterState(StatesGroup):

    username = State()
    email = State()
    first_name = State()
    last_name = State()
    phone = State()
    address = State()
    password = State()
    confirm_password = State()


class LoginState(StatesGroup):

    username = State()
    password = State()
    token = State()

    next_page_number = State()
    user_id = State()
    message_to_product_id = State()

    categories = State()
    categories_slug_list = State()


class ResetPasswordState(StatesGroup):

    email = State()
