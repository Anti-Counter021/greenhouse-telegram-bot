from dispatcher import bot

from server_requests import HOST


async def load_products(products, user_id):
    for product in products:
        price = f'{product["price"]} руб.' if not product["discount"] else \
            f'<del>{product["price"]}</del> <strong>-{product["discount"]}%</strong>\n' \
            f'{product["price_with_discount"]} руб.'
        await bot.send_message(
            user_id,
            f'{product["title"]}\n'
            f'{price}\n'
            f'{product["description"]}'
        )
        await bot.send_message(user_id, HOST + "/products/" + product["slug"])
