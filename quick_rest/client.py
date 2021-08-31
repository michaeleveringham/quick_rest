import requests
from requests.models import Response
import json
from csv import DictWriter
from typing import Any
from .exceptions import ServerError, ArgumentError, FormatError
from .resources import strdict


class ServerResponse():
    def __init__(self, response: Response, encoding: str = 'utf-8',
                 values_key = '') -> None:
        self.requests_response = response
        self.raw_content = response.content
        self.encoding = encoding
        self.values_key = values_key

    def decode(self, encoding: str = '') -> dict:
        if not encoding:
            encoding = self.encoding
        return json.loads((self.raw_content).decode(encoding))

    def get_value(self, key: str = '') -> Any:
        if not key:
            if not self.values_key:
                raise ArgumentError(('Use either a "key" kwarg in "get_value"'
                                     ' or initialise client with "values_key".'))
            else:
                key = self.values_key
        return self.decode()[key]

    def to_csv(self, export_path: str, lineterminator: str = '\n',
               omit_header: bool = False) -> None:
        response = self.decode()
        if len(response) == 1 and isinstance(response, dict):
            data = response[list(response.keys())[0]]
        else:
            raise FormatError(('The server response is either not a dict or is'
                               ' a dict with multiple keys. Response is length'
                               f' {len(response)} and type {type(response)}.'))
        fields = data[0].keys()
        with open(export_path, 'w', encoding=self.encoding) as csv_file:
            writer = DictWriter(csv_file, fieldnames=fields,
                                lineterminator=lineterminator)
            if not omit_header:
                writer.writeheader()
            for i in data:
                writer.writerow(i)

    def to_txt(self, export_path: str) -> None:
        with open(export_path, 'wb') as txt_file:
            txt_file.write(self.raw_content)


class Client():
    def __init__(self, url: str, encoding: str = 'utf-8', verify: bool = True,
                 values_key: str = '', ignore_errors: bool = False) -> None:
        self.url = url
        self.encoding = encoding
        self.ignore_errors = ignore_errors
        self.verify = verify
        if not verify:
            requests.packages.urllib3.disable_warnings(
                requests.packages.urllib3.exceptions.InsecureRequestWarning
                )
        self.values_key = values_key

    def _sanitize_kwargs(self, kwargs):
        headers = {}
        if 'headers' in kwargs.keys():
            headers.update(kwargs.pop('headers'))
        return headers, kwargs

    def _handle_response(self, response: Response) -> ServerResponse:
        code = str(response.status_code)[:1]
        if code not in ('2', '3') and not self.ignore_errors:
            raise ServerError(f'{response.status_code}: {response.reason} {response.text}')
        else:
            return ServerResponse(response, encoding=self.encoding,
                                  values_key=self.values_key)

    def _call_api_get(self, route: str, **kwargs) -> ServerResponse:
        url = f'{self.url}{route}'
        response = requests.get(url, verify=self.verify, **kwargs)
        return self._handle_response(response)

    def _call_api_post(self, route: str, json_data: dict = {},
                       text_data: str = '', **kwargs) -> ServerResponse:
        url = f'{self.url}{route}'
        if json_data:
            response = requests.post(url, json=json_data, verify=self.verify, **kwargs)
        elif text_data:
            headers = {}
            if 'headers' in kwargs.keys():
                headers.update(kwargs.pop('headers'))
            headers["Content-Type"] = "text/plain"
            response = requests.post(url, data=text_data, verify=self.verify, **kwargs)
        else:
            response = requests.post(url, verify=self.verify, **kwargs)
        return self._handle_response(response)

    def get(self, route: str, **kwargs) -> ServerResponse:
        return self._call_api_get(route, **kwargs)

    def post(self, route: str, data: strdict = '', **kwargs) -> ServerResponse:
        if isinstance(data, dict):
            return self._call_api_post(route, json_data=data, **kwargs)
        elif isinstance(data, str):
            return self._call_api_post(route, text_data=data, **kwargs)
        else:
            raise TypeError('Argument "data" must be of type "str" or "dict".')
