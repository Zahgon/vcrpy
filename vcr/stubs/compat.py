import http.client
from io import BytesIO

"""
The python3 http.client api moved some stuff around, so this is an abstraction
layer that tries to cope with this move.
"""


def get_header(message, name):
    pass


def get_header_items(message):
    pass


def get_headers(message):
    pass


def get_httpmessage(headers):
    return http.client.parse_headers(BytesIO(headers))
