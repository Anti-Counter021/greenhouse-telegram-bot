from server_requests.base_request import AbstractRequest


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


request_cart = CartRequest
