import functools
import logging
from collections import defaultdict

from httpcore import Response
from httpcore._models import ByteStream

from vcr.errors import CannotOverwriteExistingCassetteException
from vcr.filters import decode_response
from vcr.request import Request as VcrRequest
from vcr.serializers.compat import convert_body_to_bytes

_logger = logging.getLogger(__name__)


def _serialize_headers(real_response):
    """
    Some headers can appear multiple times, like "Set-Cookie".
    Therefore serialize every header key to a list of values.
    """
    pass


def _serialize_response(real_response, real_response_content):
    # The reason_phrase may not exist
    pass


def _deserialize_headers(headers):
    """
    httpcore accepts headers as list of tuples of header key and value.
    """
    pass


def _deserialize_response(vcr_response):
    # Cassette format generated for HTTPX requests by older versions of
    # vcrpy. We restructure the content to resemble what a regular
    # cassette looks like.
    pass


def _make_vcr_request(real_request, real_request_body):
    pass


def _vcr_request(cassette, real_request, real_request_body):
    pass


def _record_responses(cassette, vcr_request, real_response, real_response_content):
    pass


def _play_responses(cassette, vcr_request):
    pass


async def _vcr_handle_async_request(cassette, real_handle_async_request, self, real_request):
    # Reading the request stream consumes the iterator, so we need to restore it afterwards
    pass


def vcr_handle_async_request(cassette, real_handle_async_request):
    @functools.wraps(real_handle_async_request)
    pass


def _vcr_handle_request(cassette, real_handle_request, self, real_request):
    # Reading the request stream consumes the iterator, so we need to restore it afterwards
    pass


def vcr_handle_request(cassette, real_handle_request):
    @functools.wraps(real_handle_request)
    pass
