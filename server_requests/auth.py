from .base_request import AbstractRequest


class LoginRequest(AbstractRequest):

    url = 'auth/token'


request_login = LoginRequest()
