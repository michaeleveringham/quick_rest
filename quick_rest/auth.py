from quick_rest.client import Client, ServerResponse
from quick_rest.exceptions import TokenError
from quick_rest.resources import strdict



class BasicClient(Client):
    def __init__(
        self,
        url: str,
        credentials: dict,
        encoding: str = 'utf-8',
        verify: bool = True
    ) -> None:
        super().__init__(url, encoding=encoding, verify=verify)
        self.credentials = credentials

class KeyClient(BasicClient):
    def __init__(
        self,
        url: str,
        credentials: dict,
        encoding: str = 'utf-8',
        verify: bool = True
    ) -> None:
        super().__init__(
            url,
            credentials=credentials,
            encoding=encoding,
            verify=verify
        )

    def get(self, route: str, **kwargs) -> ServerResponse:
        headers, kwargs = self._sanitize_kwargs(kwargs)
        headers = {**self.credentials, **headers}
        return super().get(route, headers=headers, **kwargs)

    def post(self, route: str, data: strdict = '', **kwargs) -> ServerResponse:
        headers, kwargs = self._sanitize_kwargs(kwargs)
        headers = {**self.credentials, **headers}
        return super().post(route, data, headers=headers, **kwargs)


class JWTClient(Client):
    def __init__(
        self,
        url: str,
        credentials: dict,
        auth_route: str,
        token_name: str,
        jwt_key_name: str,
        encoding: str = 'utf-8',
        jwt_prefix: str = '',
        verify: bool = True
    ) -> None:
        super().__init__(url, encoding=encoding, verify=verify)
        self.jwt_key_name = jwt_key_name
        self.jwt_prefix = jwt_prefix
        self.auths = (auth_route, token_name, credentials)

    def _authenticate(
        self,
        auth_route: str,
        token_name: str,
        credentials: dict
    ) -> str:
        token_dict = self._call_api_post(
            auth_route,
            json_data=credentials
        ).decode()
        if token_name in token_dict:
            return str(token_dict[token_name])
        else:
            error = (
                'Token not found or invalid token name '
                f'"{token_name}".\nServer response: {token_dict}'
            )
            raise TokenError(error)

    def _get_jwt(self) -> dict:
        jwt = self._authenticate(*self.auths)
        if self.jwt_prefix:
            return {self.jwt_key_name: f'{self.jwt_prefix}{jwt}'}
        else:
            return {self.jwt_key_name: jwt}

    def get(self, route: str, **kwargs) -> ServerResponse:
        headers, kwargs = self._sanitize_kwargs(kwargs)
        headers = {**self._get_jwt(), **headers}
        return super().get(route, headers=headers, **kwargs)

    def post(self, route: str, data: strdict = '', **kwargs) -> ServerResponse:
        headers, kwargs = self._sanitize_kwargs(kwargs)
        headers = {**self._get_jwt(), **headers}
        return super().post(route, data, headers=headers, **kwargs)


class OAuthClient(JWTClient):
    def __init__(
        self,
        url: str,
        auth_route: str,
        token_name: str,
        credentials: dict,
        encoding: str = 'utf-8'
    ):
        raise NotImplementedError('OAuth not yet supported.')
