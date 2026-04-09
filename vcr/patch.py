"""Utilities for patching in cassettes"""

import contextlib
import functools
import http.client as httplib
import itertools
import logging
from unittest import mock

from .stubs import VCRHTTPConnection, VCRHTTPSConnection

log = logging.getLogger(__name__)
# Save some of the original types for the purposes of unpatching
_HTTPConnection = httplib.HTTPConnection
_HTTPSConnection = httplib.HTTPSConnection

# Try to save the original types for boto3
try:
    from botocore.awsrequest import AWSHTTPConnection, AWSHTTPSConnection
except ImportError as e:
    try:
        import botocore.vendored.requests  # noqa: F401
    except ImportError:  # pragma: no cover
        pass
    else:
        raise RuntimeError(
            "vcrpy >=4.2.2 and botocore <1.11.0 are not compatible"
            "; please upgrade botocore (or downgrade vcrpy)",
        ) from e
else:
    _Boto3VerifiedHTTPSConnection = AWSHTTPSConnection
    _cpoolBoto3HTTPConnection = AWSHTTPConnection
    _cpoolBoto3HTTPSConnection = AWSHTTPSConnection

cpool = None
conn = None
# Try to save the original types for urllib3
try:
    import urllib3.connection as conn
    import urllib3.connectionpool as cpool
except ImportError:  # pragma: no cover
    pass
else:
    _VerifiedHTTPSConnection = conn.VerifiedHTTPSConnection
    _connHTTPConnection = conn.HTTPConnection
    _connHTTPSConnection = conn.HTTPSConnection

# Try to save the original types for requests
try:
    import requests
except ImportError:  # pragma: no cover
    pass
else:
    if requests.__build__ < 0x021602:
        raise RuntimeError(
            "vcrpy >=4.2.2 and requests <2.16.2 are not compatible"
            "; please upgrade requests (or downgrade vcrpy)",
        )


# Try to save the original types for httplib2
try:
    import httplib2
except ImportError:  # pragma: no cover
    pass
else:
    _HTTPConnectionWithTimeout = httplib2.HTTPConnectionWithTimeout
    _HTTPSConnectionWithTimeout = httplib2.HTTPSConnectionWithTimeout
    _SCHEME_TO_CONNECTION = httplib2.SCHEME_TO_CONNECTION

# Try to save the original types for Tornado
try:
    import tornado.simple_httpclient
except ImportError:  # pragma: no cover
    pass
else:
    _SimpleAsyncHTTPClient_fetch_impl = tornado.simple_httpclient.SimpleAsyncHTTPClient.fetch_impl

try:
    import tornado.curl_httpclient
except ImportError:  # pragma: no cover
    pass
else:
    _CurlAsyncHTTPClient_fetch_impl = tornado.curl_httpclient.CurlAsyncHTTPClient.fetch_impl

try:
    import aiohttp.client
except ImportError:  # pragma: no cover
    pass
else:
    _AiohttpClientSessionRequest = aiohttp.client.ClientSession._request


try:
    import httpcore
except ImportError:  # pragma: no cover
    pass
else:
    _HttpcoreConnectionPool_handle_request = httpcore.ConnectionPool.handle_request
    _HttpcoreAsyncConnectionPool_handle_async_request = httpcore.AsyncConnectionPool.handle_async_request


class CassettePatcherBuilder:
    def _build_patchers_from_mock_triples_decorator(function):
        @functools.wraps(function)
        pass

    def __init__(self, cassette):
        self._cassette = cassette
        self._class_to_cassette_subclass = {}

    def build(self):
        pass

    def _build_patchers_from_mock_triples(self, mock_triples):
        pass

    def _build_patcher(self, obj, patched_attribute, replacement_class):
        pass

    def _recursively_apply_get_cassette_subclass(self, replacement_dict_or_obj):
        """One of the subtleties of this class is that it does not directly
        replace HTTPSConnection with `VCRRequestsHTTPSConnection`, but a
        subclass of the aforementioned class that has the `cassette`
        class attribute assigned to `self._cassette`. This behavior is
        necessary to properly support nested cassette contexts.

        This function exists to ensure that we use the same class
        object (reference) to patch everything that replaces
        VCRRequestHTTP[S]Connection, but that we can talk about
        patching them with the raw references instead, and without
        worrying about exactly where the subclass with the relevant
        value for `cassette` is first created.

        The function is recursive because it looks in to dictionaries
        and replaces class values at any depth with the subclass
        described in the previous paragraph.
        """
        pass

    def _get_cassette_subclass(self, klass):
        pass

    def _build_cassette_subclass(self, base_class):
        pass

    @_build_patchers_from_mock_triples_decorator
    def _httplib(self):
        pass

    def _requests(self):
        pass

    @_build_patchers_from_mock_triples_decorator
    def _boto3(self):
        pass

    def _patched_get_conn(self, connection_pool_class, connection_class_getter):
        pass

    def _patched_new_conn(self, connection_pool_class, connection_remover):
        pass

    def _urllib3(self):
        pass

    @_build_patchers_from_mock_triples_decorator
    def _httplib2(self):
        pass

    @_build_patchers_from_mock_triples_decorator
    def _tornado(self):
        pass

    @_build_patchers_from_mock_triples_decorator
    def _aiohttp(self):
        pass

    @_build_patchers_from_mock_triples_decorator
    def _httpcore(self):
        pass

    def _urllib3_patchers(self, cpool, conn, stubs):
        pass


class ConnectionRemover:
    def __init__(self, connection_class):
        self._connection_class = connection_class
        self._connection_pool_to_connections = {}

    def add_connection_to_pool_entry(self, pool, connection):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        for pool, connections in self._connection_pool_to_connections.items():
            readd_connections = []
            while pool.pool and not pool.pool.empty() and connections:
                connection = pool.pool.get()
                if isinstance(connection, self._connection_class):
                    connections.remove(connection)
                    connection.close()
                else:
                    readd_connections.append(connection)
            for connection in readd_connections:
                pool._put_conn(connection)
            for connection in connections:
                connection.close()


def reset_patchers():
    pass


@contextlib.contextmanager
def force_reset():
    pass
