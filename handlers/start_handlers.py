from aiogram import types

from dispatcher import dispatcher
from states import LoginState, MakeOrderState, ReviewState
from server_requests import HOST


commands = """
\t\t\t\t\t\t\t\t <strong>Многие команды после выбора остановить нельзя (регистрация...)</strong>

\t\t\t\t\t\t\t\t <strong>Команды пользователя</strong>
/login - Авторизация (только не авторизованным пользователям)
/register - Регистрация нового пользователя (только не авторизованным пользователям)
/reset_password - Отправка email для сброса пароля пользователя (только не авторизованным пользователям)
/logout - Выход (только авторизованным пользователям)
/profile - Заказы пользователя (только авторизованным пользователям)

\t\t\t\t\t\t\t\t <strong>Команды корзины</strong>
/cart - Корзина (только авторизованным пользователям)
/add - Добавить товар в корзину. Этой командой необходимо ответить на сообщение с товаром (только авторизованным пользователям)
/remove - Удалить товар из корзины. Этой командой необходимо ответить на сообщение с товаром в корзине (только авторизованным пользователям)
/change - Изменить количество товара в корзине. Этой командой необходимо ответить на сообщение с товаром в корзине и написать на какое количество вы хотите изменить этот товар (только авторизованным пользователям)
/make - Оформить заказ (только авторизованным пользователям)

\t\t\t\t\t\t\t\t <strong>Команды для вывода товаров с магазина</strong>
/categories - Категории
/products - Товары
/detail - Детализация товара. Этой командой необходимо ответить на сообщение с товаром

\t\t\t\t\t\t\t\t <strong>Команды отзывов</strong>
/reviews - Отзывы
/new_review - Добавить отзыв (только авторизованным пользователям)

\t\t\t\t\t\t\t\t <strong>Остальные команды</strong>
/help - Помощь
/link - Ссылка на наш сайт
/feedback - Обратная связь (ошибки, пожелания)
/dev - Информация о разработчике
"""


@dispatcher.message_handler(commands=['dev'], state=[None, LoginState, MakeOrderState, ReviewState])
async def about_developer(message: types.Message):
    await message.answer(
        'Привет! Меня зовут _Counter021_. Я разработчик этого бота и сайта.\n'
        'Это мой только 4 бот. Надеюсь вам он понравится.\n'
        'Оба этих проектов я делал в одиночку, поэтому прошу, если у вас возник баг воспользуйтесь средствами обратной '
        'связи, напишите в чём возникла проблема.\n'
        'Если кому-то интересно. Мой GitHub:\n'
        'https://github.com/Counter0021'
    )


@dispatcher.message_handler(commands=['help'], state=[None, LoginState, MakeOrderState, ReviewState])
async def help_bot(message: types.Message):
    await message.answer(commands)


@dispatcher.message_handler(commands=['link'], state=[None, LoginState, MakeOrderState, ReviewState])
async def link(message: types.Message):
    await message.answer(f'Ссылка на наш сайт {HOST}')


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f'Приветствую @{message.from_user.username}!\n'
        f'Я Greenhouse Bot от сайта по продаже теплиц. Вы можете получить подробную информацию обо мне командой /help.\n'
    )
