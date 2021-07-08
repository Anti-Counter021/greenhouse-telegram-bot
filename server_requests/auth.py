from .base_request import AbstractRequest


class AuthMixin(AbstractRequest):

    def exists_username(self, username) -> str:
        self.url = 'auth/username'
        return self.post_json({'username': username})


class RegisterRequest(AuthMixin):

    def register(self, data):
        self.url = 'auth/register'
        return self.post_json(data)


class LoginRequest(AuthMixin):

    def login(self, data):
        self.url = 'auth/token'
        return self.post_json(data)


class LogoutRequest(AbstractRequest):

    url = 'auth/logout'

    def __init__(self, token):
        self.headers = {**self.headers, 'Authorization': f'Token {token}'}
        super().__init__()


class ProfileRequest(AbstractRequest):

    url = 'auth/profile'

    def __init__(self, token):
        self.headers = {**self.headers, 'Authorization': f'Token {token}'}
        super().__init__()


request_login = LoginRequest()
request_register = RegisterRequest()
profile_request = ProfileRequest
logout_request = LogoutRequest
