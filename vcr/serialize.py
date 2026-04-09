import yaml

from vcr.request import Request
from vcr.serializers import compat

# version 1 cassettes started with VCR 1.0.x.
# Before 1.0.x, there was no versioning.
CASSETTE_FORMAT_VERSION = 1

"""
Just a general note on the serialization philosophy here:
I prefer cassettes to be human-readable if possible.  Yaml serializes
bytestrings to !!binary, which isn't readable, so I would like to serialize to
strings and from strings, which yaml will encode as utf-8 automatically.
All the internal HTTP stuff expects bytestrings, so this whole serialization
process feels backwards.

Serializing: bytestring -> string (yaml persists to utf-8)
Deserializing: string (yaml converts from utf-8) -> bytestring
"""


def _looks_like_an_old_cassette(data):
    pass


def _warn_about_old_cassette_format():
    raise ValueError(
        "Your cassette files were generated in an older version "
        "of VCR. Delete your cassettes or run the migration script."
        "See http://git.io/mHhLBg for more details.",
    )


def deserialize(cassette_string, serializer):
    pass


def serialize(cassette_dict, serializer):
    pass
