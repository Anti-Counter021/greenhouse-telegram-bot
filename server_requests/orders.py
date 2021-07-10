from .base_request import AbstractRequest


class OrderRequest(AbstractRequest):

    url = 'orders/'

    def __init__(self, token):
        self.headers = {**self.headers, 'Authorization': f'Token {token}'}
        super().__init__()


request_order = OrderRequest
