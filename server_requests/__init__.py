HOST: str = 'http://localhost:8000'
SITE: str = HOST + '/api/'

from .categories import request_categories
from .products import request_products
from .auth import request_login, profile_request, logout_request, request_register, request_reset_password
from .cart import request_cart
from .order import request_order
