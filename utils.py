from typing import Dict, List

from dispatcher import bot
from server_requests import HOST


async def product_detail_load(product: Dict, user_id: int) -> int:

    price = f'{product["price"]} руб.' if not product["discount"] else \
        f'<del>{product["price"]}</del> <strong>-{product["discount"]}%</strong>\n' \
        f'{product["price_with_discount"]} руб.'

    message = await bot.send_message(
        user_id,
        f'{product["title"]}\n'
        f'{price}\n'
        f'{product["description"]}'
    )

    await bot.send_message(user_id, HOST + "/products/" + product["slug"])
    return message.message_id


async def load_products(products: List[Dict], user_id: int):
    message_to_product_id: Dict[int, str] = {}

    for product in products:
        message_id = await product_detail_load(product, user_id)
        message_to_product_id[message_id] = product['slug']

    return message_to_product_id
