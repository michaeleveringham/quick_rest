
# `quick_rest`
A simple utility for any REST API, regardless of authentication type.

## Why?
Some have asked me why bother when there are so many packages for interacting with REST APIs already.

This is exactly partially why for me, though. I've found every vendor has their own REST API Python package it seems and I just wanted one package to use for all my REST API interfaces.

I'm sure that there are better packages that achieve my goal already but this is the other part of why for me: I just wanted to.

## Dependencies
`quick_rest` would be nothing without [requests](https://pypi.org/project/requests/). It is an amazing module and the only dependency that isn't built-in with Python and is the backbone of the project.

## Installation
Use pip to install.
`python -m pip install quick_rest`

## Usage
There isn't much to this package so I haven't written full documentation yet.

You can get and post right now, and use the auth methods listed below. You can pass any `requests` `get` or `post` kwarg in on the `Client.get` and `Client.post` methods.

### Authentication
You can currently use no authentication, key authentication and JWT authentication. OAuth is a work in progress, please suggest other authentication types to add.

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
#### OAuth
``` python
# Coming soon
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
Please make any suggestions or issues on the Github page. Remember I'm just one person but I'll try to be as quick as I can.

## License
This project is licensed under the MIT License. Please see the LICENSE.md file for details.
