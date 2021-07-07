from .base_request import AbstractRequest


class CategoriesRequest(AbstractRequest):

    url = 'categories/'


request_categories = CategoriesRequest()
