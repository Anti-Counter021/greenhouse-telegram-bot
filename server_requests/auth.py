from .base_request import AbstractRequest


class LoginRequest(AbstractRequest):

    def exists_username(self, username) -> str:
        self.url = 'auth/username'
        return self.post_json(username)

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
profile_request = ProfileRequest
logout_request = LogoutRequest
