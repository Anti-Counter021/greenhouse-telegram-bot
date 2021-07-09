from .base_request import AbstractRequest


class AuthMixin(AbstractRequest):

    def exists_username(self, username) -> str:
        self.url = 'auth/username'
        return self.post_json({'username': username})

    def exists_email(self, email) -> str:
        self.url = 'auth/email'
        return self.post_json({'email': email})


class RegisterRequest(AuthMixin):

    def register(self, data) -> str:
        self.url = 'auth/register'
        return self.post_json(data)


class ResetPasswordRequest(AuthMixin):

    def reset_password(self, email) -> str:
        self.url = 'auth/password/reset/'
        return self.post_json({'email': email})


class LoginRequest(AuthMixin):

    def login(self, data) -> str:
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
request_reset_password = ResetPasswordRequest()
profile_request = ProfileRequest
logout_request = LogoutRequest
