def convert_to_bytes(resp):
    pass


def convert_to_unicode(resp):
    pass


def convert_body_to_bytes(resp):
    """
    If the request body is a string, encode it to bytes (for python3 support)

    By default yaml serializes to utf-8 encoded bytestrings.
    When this cassette is loaded by python3, it's automatically decoded
    into unicode strings. This makes sure that it stays a bytestring, since
    that's what all the internal httplib machinery is expecting.

    For more info on py3 yaml:
    http://pyyaml.org/wiki/PyYAMLDocumentation#Python3support
    """
    pass


def _convert_string_to_unicode(string):
    """
    If the string is bytes, decode it to a string (for python3 support)
    """
    pass


def convert_body_to_unicode(resp):
    """
    If the request or responses body is bytes, decode it to a string
    (for python3 support)
    """
    pass
