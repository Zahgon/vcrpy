import logging
import warnings
from contextlib import suppress
from io import BytesIO
from urllib.parse import parse_qsl, urlparse

from .util import CaseInsensitiveDict, _is_nonsequence_iterator

log = logging.getLogger(__name__)


class Request:
    """
    VCR's representation of a request.
    """

    def __init__(self, method, uri, body, headers):
        self.method = method
        self.uri = uri
        self._was_file = hasattr(body, "read")
        self._was_iter = _is_nonsequence_iterator(body)
        if self._was_file:
            if hasattr(body, "tell"):
                tell = body.tell()
                self.body = body.read()
                body.seek(tell)
            else:
                self.body = body.read()
        elif self._was_iter:
            self.body = list(body)
        else:
            self.body = body
        self.headers = headers
        log.debug("Invoking Request %s", self.uri)

    @property
    def uri(self):
        pass

    @uri.setter
    def uri(self, uri):
        pass

    @property
    def headers(self):
        pass

    @headers.setter
    def headers(self, value):
        pass

    @property
    def body(self):
        pass

    @body.setter
    def body(self, value):
        pass

    def add_header(self, key, value):
        pass

    @property
    def scheme(self):
        pass

    @property
    def host(self):
        pass

    @property
    def port(self):
        pass

    @property
    def path(self):
        pass

    @property
    def query(self):
        pass

    # alias for backwards compatibility
    @property
    def url(self):
        pass

    # alias for backwards compatibility
    @property
    def protocol(self):
        pass

    def __str__(self):
        return f"<Request ({self.method}) {self.uri}>"

    def __repr__(self):
        return self.__str__()

    def _to_dict(self):
        pass

    @classmethod
    def _from_dict(cls, dct):
        pass


class HeadersDict(CaseInsensitiveDict):
    """
    There is a weird quirk in HTTP.  You can send the same header twice.  For
    this reason, headers are represented by a dict, with lists as the values.
    However, it appears that HTTPlib is completely incapable of sending the
    same header twice.  This puts me in a weird position: I want to be able to
    accurately represent HTTP headers in cassettes, but I don't want the extra
    step of always having to do [0] in the general case, i.e.
    request.headers['key'][0]

    In addition, some servers sometimes send the same header more than once,
    and httplib *can* deal with this situation.

    Furthermore, I wanted to keep the request and response cassette format as
    similar as possible.

    For this reason, in cassettes I keep a dict with lists as keys, but once
    deserialized into VCR, I keep them as plain, naked dicts.
    """

    def __setitem__(self, key, value):
        if isinstance(value, (tuple, list)):
            value = value[0]

        # Preserve the case from the first time this key was set.
        old = self._store.get(key.lower())
        if old:
            key = old[0]

        super().__setitem__(key, value)
