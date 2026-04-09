import copy
import json
import zlib
from io import BytesIO
from urllib.parse import urlencode, urlparse, urlunparse

from .util import CaseInsensitiveDict

try:
    # This supports both brotli & brotlipy packages
    import brotli
except ImportError:
    try:
        import brotlicffi as brotli
    except ImportError:
        brotli = None


def decompress_deflate(body):
    pass


def decompress_gzip(body):
    # To (de-)compress gzip format, use wbits = zlib.MAX_WBITS | 16.
    pass


AVAILABLE_DECOMPRESSORS = {
    "deflate": decompress_deflate,
    "gzip": decompress_gzip,
}

if brotli is not None:

    def decompress_brotli(body):
        pass

    AVAILABLE_DECOMPRESSORS["br"] = decompress_brotli


def replace_headers(request, replacements):
    """Replace headers in request according to replacements.
    The replacements should be a list of (key, value) pairs where the value can be any of:
    1. A simple replacement string value.
    2. None to remove the given header.
    3. A callable which accepts (key, value, request) and returns a string value or None.
    """
    pass


def remove_headers(request, headers_to_remove):
    """
    Wrap replace_headers() for API backward compatibility.
    """
    pass


def replace_query_parameters(request, replacements):
    """Replace query parameters in request according to replacements.

    The replacements should be a list of (key, value) pairs where the value can be any of:
      1. A simple replacement string value.
      2. None to remove the given header.
      3. A callable which accepts (key, value, request) and returns a string
         value or None.
    """
    pass


def remove_query_parameters(request, query_parameters_to_remove):
    """
    Wrap replace_query_parameters() for API backward compatibility.
    """
    pass


def replace_post_data_parameters(request, replacements):
    """Replace post data in request--either form data or json--according to replacements.

    The replacements should be a list of (key, value) pairs where the value can be any of:
      1. A simple replacement string value.
      2. None to remove the given header.
      3. A callable which accepts (key, value, request) and returns a string
         value or None.
    """
    pass


def remove_post_data_parameters(request, post_data_parameters_to_remove):
    """
    Wrap replace_post_data_parameters() for API backward compatibility.
    """
    pass


def decode_response(response):
    """
    If the response is compressed with any supported compression (gzip,
    deflate, br if available):
      1. decompress the response body
      2. delete the content-encoding header
      3. update content-length header to decompressed length
    """
    pass
