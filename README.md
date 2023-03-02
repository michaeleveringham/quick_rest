
# `quick_rest`

A versatile wrapper for REST APIs.

## Dependencies

The sole non-builtin dependency is [requests](https://pypi.org/project/requests/).

## Installation

Use pip to install.

```
python -m pip install quick_rest
```

## Usage

No full documentation at this time, maybe someday I'll get around to it...

You can get and post right now, and use the auth methods listed below. You can pass any `requests` `get` or `post` kwarg in on the `Client.get` and `Client.post` methods.

### Authentication

You can currently use no authentication, key authentication and JWT authentication.

#### No Authentication

``` python
from quick_rest import Client

url = 'https://cat-fact.herokuapp.com/'
client = Client(url)
route = 'facts'
response = client.get(route)
```

#### Key

``` python
from quick_rest import KeyClient

url = 'https://www.haloapi.com/'
creds = {'keyname': 'somekeyhere'}
client = KeyClient(url, creds)
route = 'stats/hw2/xp?players=LamerLink' # check out my sweet Halo stats
response = client.get(route)
```

#### JWT (JSON Web Token)

``` python
from quick_rest import JWTClient

url = 'https://some-jwt-client.com/'
creds = {'username': 'someusername', 'password': 'somepassword'}
# We need to specify the names for the auth_route, token_name, and jwt_key_name.
client = JWTClient(url, creds, 'auth', 'access_token', 'Authorization')
route = 'v0/some/route/results.json'
response = client.get(route)
```

### Results

Results come in the form of a `ServerResponse` object. You can access the `raw_content` attribute or use the `decode`, `get_value`, `to_txt` and `to_csv` methods to get the data from the object.

``` python
raw_response = response.raw_response
decoded_response = response.decode() # utf-8 by default
decoded_response = response.decode(encoding='utf-16')
value = response.get_value(key_name)
response.to_txt('some/path/file.txt') # dumps the raw response to file
response.to_csv('some/path/file.csv')
# By default, to_csv sets \n to lineterminator and writes the header to file
response.to_csv('some/path/file.csv', lineterminator='\t', omit_header=True)
```

## Issues/Suggestions
Please make any suggestions or issues on the Github page.

## To Do

* Tests.
* Oauth client.

## License
This project is licensed under the MIT License. Please see the LICENSE.md file for details.
