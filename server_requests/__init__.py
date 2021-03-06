HOST: str = 'http://localhost'
SITE: str = HOST + '/api/'

from .categories import request_categories
from .products import request_products
from .auth import request_login, profile_request, logout_request, request_register, request_reset_password
from .cart import request_cart
from .orders import request_order
from .feedback import request_feedback
from .reviews import request_review
