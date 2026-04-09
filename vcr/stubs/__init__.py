"""Stubs for patching HTTP and HTTPS requests"""

import logging
from contextlib import suppress
from http.client import HTTPConnection, HTTPResponse, HTTPSConnection
from io import BytesIO

from vcr.errors import CannotOverwriteExistingCassetteException
from vcr.request import Request

from . import compat

log = logging.getLogger(__name__)


class VCRFakeSocket:
    """
    A socket that doesn't do anything!
    Used when playing back cassettes, when there
    is no actual open socket.
    """

    def close(self):
        pass

    def settimeout(self, *args, **kwargs):
        pass

    def fileno(self):
        """
        This is kinda crappy.  requests will watch
        this descriptor and make sure it's not closed.
        Return file descriptor 0 since that's stdin.
        """
        pass


def parse_headers(header_list):
    """
    Convert headers from our serialized dict with lists for keys to a
    HTTPMessage
    """
    header_string = b""
    for key, values in header_list.items():
        for v in values:
            header_string += key.encode("utf-8") + b":" + v.encode("utf-8") + b"\r\n"
    return compat.get_httpmessage(header_string)


def serialize_headers(response):
    pass


class VCRHTTPResponse(HTTPResponse):
    """
    Stub response class that gets returned instead of a HTTPResponse
    """

    def __init__(self, recorded_response):
        self.fp = None
        self.recorded_response = recorded_response
        self.reason = recorded_response["status"]["message"]
        self.status = self.code = recorded_response["status"]["code"]
        self.version = None
        self.version_string = None
        self._content = BytesIO(self.recorded_response["body"]["string"])
        self._closed = False
        self._original_response = self  # for requests.session.Session cookie extraction

        headers = self.recorded_response["headers"]
        # Since we are loading a response that has already been serialized, our
        # response is no longer chunked.  That means we don't want any
        # libraries trying to process a chunked response.  By removing the
        # transfer-encoding: chunked header, this should cause the downstream
        # libraries to process this as a non-chunked response.
        te_key = [h for h in headers if h.upper() == "TRANSFER-ENCODING"]
        if te_key:
            del headers[te_key[0]]
        self.headers = self.msg = parse_headers(headers)

        self.length = compat.get_header(self.msg, "content-length") or None

    @property
    def closed(self):
        # in python3, I can't change the value of self.closed.  So I'
        # twiddling self._closed and using this property to shadow the real
        # self.closed from the superclass
        pass

    def read(self, *args, **kwargs):
        return self._content.read(*args, **kwargs)

    def read1(self, *args, **kwargs):
        pass

    def readall(self):
        pass

    def readinto(self, *args, **kwargs):
        pass

    def readline(self, *args, **kwargs):
        pass

    def readlines(self, *args, **kwargs):
        pass

    def seekable(self):
        pass

    def tell(self):
        pass

    def isatty(self):
        pass

    def seek(self, *args, **kwargs):
        return self._content.seek(*args, **kwargs)

    def close(self):
        self._closed = True
        return True

    def getcode(self):
        pass

    def isclosed(self):
        pass

    def info(self):
        return parse_headers(self.recorded_response["headers"])

    def getheaders(self):
        pass

    def getheader(self, header, default=None):
        pass

    def readable(self):
        pass

    @property
    def length_remaining(self):
        pass

    def get_redirect_location(self):
        """
        Returns (a) redirect location string if we got a redirect
        status code and valid location, (b) None if redirect status and
        no location, (c) False if not a redirect status code.
        See https://urllib3.readthedocs.io/en/stable/reference/urllib3.response.html .
        """
        pass

    @property
    def data(self):
        pass

    def drain_conn(self):
        pass

    def stream(self, amt=65536, decode_content=None):
        pass


class VCRConnection:
    # A reference to the cassette that's currently being patched in
    cassette = None

    def _port_postfix(self):
        """
        Returns empty string for the default port and ':port' otherwise
        """
        port = (
            self.real_connection.port
            if not self.real_connection._tunnel_host
            else self.real_connection._tunnel_port
        )
        default_port = {"https": 443, "http": 80}[self._protocol]
        return f":{port}" if port != default_port else ""

    def _real_host(self):
        """Returns the request host"""
        if self.real_connection._tunnel_host:
            # The real connection is to an HTTPS proxy
            return self.real_connection._tunnel_host
        else:
            return self.real_connection.host

    def _uri(self, url):
        """Returns request absolute URI"""
        if url and not url.startswith("/"):
            # Then this must be a proxy request.
            return url
        uri = f"{self._protocol}://{self._real_host()}{self._port_postfix()}{url}"
        log.debug("Absolute URI: %s", uri)
        return uri

    def _url(self, uri):
        """Returns request selector url from absolute URI"""
        pass

    def request(self, method, url, body=None, headers=None, *args, **kwargs):
        """Persist the request metadata in self._vcr_request"""
        self._vcr_request = Request(method=method, uri=self._uri(url), body=body, headers=headers or {})
        log.debug(f"Got {self._vcr_request}")

        # Note: The request may not actually be finished at this point, so
        # I'm not sending the actual request until getresponse().  This
        # allows me to compare the entire length of the response to see if it
        # exists in the cassette.

        self._sock = VCRFakeSocket()

    def putrequest(self, method, url, *args, **kwargs):
        """
        httplib gives you more than one way to do it.  This is a way
        to start building up a request.  Usually followed by a bunch
        of putheader() calls.
        """
        pass

    def putheader(self, header, *values):
        pass

    def send(self, data):
        """
        This method is called after request(), to add additional data to the
        body of the request.  So if that happens, let's just append the data
        onto the most recent request in the cassette.
        """
        pass

    def close(self):
        # Note: the real connection will only close if it's open, so
        # no need to check that here.
        self.real_connection.close()

    def endheaders(self, message_body=None):
        """
        Normally, this would actually send the request to the server.
        We are not sending the request until getting the response,
        so bypass this part and just append the message body, if any.
        """
        pass

    def getresponse(self, _=False, **kwargs):
        """Retrieve the response"""
        pass

    def set_debuglevel(self, *args, **kwargs):
        pass

    def connect(self, *args, **kwargs):
        """
        httplib2 uses this.  Connects to the server I'm assuming.

        Only pass to the baseclass if we don't have a recorded response
        and are not write-protected.
        """
        pass

    @property
    def sock(self):
        pass

    @sock.setter
    def sock(self, value):
        pass

    def __init__(self, *args, **kwargs):
        kwargs.pop("strict", None)  # apparently this is gone in py3

        # need to temporarily reset here because the real connection
        # inherits from the thing that we are mocking out.  Take out
        # the reset if you want to see what I mean :)
        from vcr.patch import force_reset

        with force_reset():
            self.real_connection = self._baseclass(*args, **kwargs)

        self._sock = None

    def __setattr__(self, name, value):
        """
        We need to define this because any attributes that are set on the
        VCRConnection need to be propagated to the real connection.

        For example, urllib3 will set certain attributes on the connection,
        such as 'ssl_version'. These attributes need to get set on the real
        connection to have the correct and expected behavior.

        TODO: Separately setting the attribute on the two instances is not
        ideal. We should switch to a proxying implementation.
        """
        with suppress(AttributeError):
            setattr(self.real_connection, name, value)

        super().__setattr__(name, value)

    def __getattr__(self, name):
        """
        Send requests for weird attributes up to the real connection
        (counterpart to __setattr above)
        """
        if self.__dict__.get("real_connection"):
            # check in case real_connection has not been set yet, such as when
            # we're setting the real_connection itself for the first time
            return getattr(self.real_connection, name)

        return super().__getattr__(name)


for k, v in HTTPConnection.__dict__.items():
    if isinstance(v, staticmethod):
        setattr(VCRConnection, k, v)


class VCRHTTPConnection(VCRConnection):
    """A Mocked class for HTTP requests"""

    _baseclass = HTTPConnection
    _protocol = "http"
    debuglevel = _baseclass.debuglevel
    _http_vsn = _baseclass._http_vsn


class VCRHTTPSConnection(VCRConnection):
    """A Mocked class for HTTPS requests"""

    _baseclass = HTTPSConnection
    _protocol = "https"
    is_verified = True
    debuglevel = _baseclass.debuglevel
    _http_vsn = _baseclass._http_vsn
