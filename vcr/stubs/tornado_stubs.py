"""Stubs for tornado HTTP clients"""

import functools
from io import BytesIO

from tornado import httputil
from tornado.httpclient import HTTPResponse

from vcr.errors import CannotOverwriteExistingCassetteException
from vcr.request import Request


def vcr_fetch_impl(cassette, real_fetch_impl):
    @functools.wraps(real_fetch_impl)
    pass
