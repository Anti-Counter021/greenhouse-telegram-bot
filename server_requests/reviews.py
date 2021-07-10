from .base_request import AbstractRequest


class ReviewRequest(AbstractRequest):

    url = 'reviews/'

    def __init__(self, token=None):
        if token is not None:
            self.headers = {**self.headers, 'Authorization': f'Token {token}'}
        super().__init__()

    def reviews(self, page: str = '1'):
        self.url = f'reviews/?page={page}'
        return self.load_json()


request_review = ReviewRequest
