from .base_request import AbstractRequest


class ProductsRequest(AbstractRequest):

    def products(self):
        self.url = 'products/'
        return self.load_json()

    def detail_product(self, slug):
        self.url = f'products/{slug}'
        return self.load_json()


request_products = ProductsRequest()
