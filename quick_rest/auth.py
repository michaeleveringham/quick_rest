from .client import Client, ServerResponse
from .exceptions import TokenError
from .resources import strdict


class BasicClient(Client):
    def __init__(self, url: str, credentials: dict, encoding: str = 'utf-8'):
        super().__init__(url, encoding=encoding)
        self.credentials = credentials

class KeyClient(BasicClient):
    def __init__(self, url: str, credentials: dict, encoding: str = 'utf-8'):
        super().__init__(url, credentials=credentials, encoding=encoding)

    def get(self, route: str, headers: dict = {}) -> ServerResponse:
        headers = {**self.credentials, **headers}
        return super().get(route, headers)

    def post(self, route: str, headers: dict = {}, data: strdict = '') -> ServerResponse:
        headers = {**self.credentials, **headers}
        return super().post(route, headers)


class JWTClient(Client):
    def __init__(self, url: str, credentials: dict, auth_route: str, token_name: str, jwt_key_name: str, encoding: str = 'utf-8') -> None:
        super().__init__(url, encoding=encoding)
        self.jwt_key_name = jwt_key_name
        self.auths = (auth_route, token_name, credentials)

    def _authenticate(self, auth_route: str, token_name: str, credentials: dict) -> str:
        token_dict = self._call_api_post(auth_route, json_data=credentials).decode()
        if token_name in token_dict:
            return str(token_dict[token_name])
        else:
            raise TokenError(f'Invalid token name: {token_name}\nServer response: {token_dict}')

    def _get_jwt(self) -> dict:
        jwt = self._authenticate(*self.auths)
        return {self.jwt_key_name: f'JWT {jwt}'}

    def get(self, route: str, headers: dict = {}) -> ServerResponse:
        headers = {**self._get_jwt(), **headers}
        return super().get(route, headers)

    def post(self, route: str, headers: dict = {}, data: strdict = '') -> ServerResponse:
        headers = {**self._get_jwt(), **headers}
        return super().post(route, headers)


class OAuthClient(JWTClient):
    def __init__(self, url: str, auth_route: str, token_name: str, credentials: dict, encoding: str = 'utf-8'):
        pass
