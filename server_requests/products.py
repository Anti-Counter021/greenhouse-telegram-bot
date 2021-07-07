from .base_request import AbstractRequest


class ProductsRequest(AbstractRequest):

    def detail_product(self, slug):
        self.url = f'products/{slug}'
        return self.load_json()

    def products(self, page: str = '1'):
        self.url = f'products/?page={page}'
        return self.load_json()


request_products = ProductsRequest()
