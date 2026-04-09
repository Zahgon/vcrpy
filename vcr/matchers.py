import json
import logging
import urllib
import xmlrpc.client
from string import hexdigits

from .util import read_body

_HEXDIG_CODE_POINTS: set[int] = {ord(s.encode("ascii")) for s in hexdigits}

log = logging.getLogger(__name__)


def method(r1, r2):
    pass


def uri(r1, r2):
    pass


def host(r1, r2):
    pass


def scheme(r1, r2):
    pass


def port(r1, r2):
    pass


def path(r1, r2):
    pass


def query(r1, r2):
    pass


def raw_body(r1, r2):
    pass


def body(r1, r2):
    pass


def headers(r1, r2):
    pass


def _header_checker(value, header="Content-Type"):
    def checker(headers):
        pass

    return checker


def _dechunk(body):
    pass


def _transform_json(body):
    pass


_xml_header_checker = _header_checker("text/xml")
_xmlrpc_header_checker = _header_checker("xmlrpc", header="User-Agent")
_checker_transformer_pairs = (
    (_header_checker("chunked", header="Transfer-Encoding"), _dechunk),
    (
        _header_checker("application/x-www-form-urlencoded"),
        lambda body: urllib.parse.parse_qs(body.decode("ascii")),
    ),
    (_header_checker("application/json"), _transform_json),
    (lambda request: _xml_header_checker(request) and _xmlrpc_header_checker(request), xmlrpc.client.loads),
)


def _get_transformers(request):
    pass


def requests_match(r1, r2, matchers):
    pass


def _evaluate_matcher(matcher_function, *args):
    """
    Evaluate the result of a given matcher as a boolean with an assertion error message if any.
    It handles two types of matcher :
    - a matcher returning a boolean value.
    - a matcher that only makes an assert, returning None or raises an assertion error.
    """
    pass


def get_matchers_results(r1, r2, matchers):
    """
    Get the comparison results of two requests as two list.
    The first returned list represents the matchers names that passed.
    The second list is the failed matchers as a string with failed assertion details if any.
    """
    pass


def get_assertion_message(assertion_details):
    """
    Get a detailed message about the failing matcher.
    """
    pass
