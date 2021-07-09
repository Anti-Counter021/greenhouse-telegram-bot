import json

from .base_request import AbstractRequest


class CartRequest(AbstractRequest):

    def __init__(self, token):
        self.headers = {**self.headers, 'Authorization': f'Token {token}'}
        super().__init__()

    def cart(self):
        self.url = 'cart/get/'
        return self.load_json()

    def add_to_cart(self, product_id):
        self.url = f'cart/add/{product_id}/'
        return self.post_json()

    def remove_product_from_cart(self, cart_product_id):
        self.url = f'cart/remove/{cart_product_id}/'
        response = self.session.delete(self.base_url + self.url)
        response.raise_for_status()
        return json.loads(response.text)

    def change_qry(self, cart_product_id, qty):
        self.url = f'cart/change-qty/{cart_product_id}/{qty}/'
        response = self.session.put(self.base_url + self.url)
        response.raise_for_status()
        return json.loads(response.text)


request_cart = CartRequest
