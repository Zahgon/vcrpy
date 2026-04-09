import yaml

# Use the libYAML versions if possible
try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader


def deserialize(cassette_string):
    pass


def serialize(cassette_dict):
    pass
