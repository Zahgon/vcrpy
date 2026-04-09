"""Stubs for aiohttp HTTP clients"""

import asyncio
import functools
import json
import logging
from collections.abc import Mapping
from http.cookies import CookieError, Morsel, SimpleCookie

from aiohttp import ClientConnectionError, ClientResponse, CookieJar, RequestInfo, hdrs, streams
from aiohttp.helpers import strip_auth_from_url
from multidict import CIMultiDict, CIMultiDictProxy, MultiDict
from yarl import URL

from vcr.errors import CannotOverwriteExistingCassetteException
from vcr.request import Request

log = logging.getLogger(__name__)


class MockStream(asyncio.StreamReader, streams.AsyncStreamReaderMixin):
    pass


class MockClientResponse(ClientResponse):
    def __init__(self, method, url, request_info=None):
        super().__init__(
            method=method,
            url=url,
            writer=None,
            continue100=None,
            timer=None,
            request_info=request_info,
            traces=None,
            loop=asyncio.get_event_loop(),
            session=None,
        )

    async def json(self, *, encoding="utf-8", loads=json.loads, **kwargs):
        stripped = self._body.strip()
        if not stripped:
            return None

        return loads(stripped.decode(encoding))

    async def text(self, encoding="utf-8", errors="strict"):
        return self._body.decode(encoding, errors=errors)

    async def read(self):
        return self._body

    def release(self):
        pass

    @property
    def content(self):
        pass


def build_response(vcr_request, vcr_response, history):
    pass


def _serialize_headers(headers):
    """Serialize CIMultiDictProxy to a pickle-able dict because proxy
    objects forbid pickling:

    https://github.com/aio-libs/multidict/issues/340
    """
    pass


def _deserialize_headers(headers):
    pass


def play_responses(cassette, vcr_request, kwargs):
    pass


async def record_response(cassette, vcr_request, response):
    """Record a VCR request-response chain to the cassette."""
    pass


async def record_responses(cassette, vcr_request, response):
    """Because aiohttp follows redirects by default, we must support
    them by default. This method is used to write individual
    request-response chains that were implicitly followed to get
    to the final destination.
    """
    pass


def _build_cookie_header(session, cookies, cookie_header, url):
    pass


def _build_url_with_params(url_str: str, params: Mapping[str, str | int | float]) -> URL:
    # This code is basically a copy&paste of aiohttp.
    # https://github.com/aio-libs/aiohttp/blob/master/aiohttp/client_reqrep.py#L225
    pass


def vcr_request(cassette, real_request):
    @functools.wraps(real_request)
    pass
