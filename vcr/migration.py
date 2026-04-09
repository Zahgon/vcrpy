"""
Migration script for old 'yaml' and 'json' cassettes

.. warning:: Backup your cassettes files before migration.

It merges and deletes the request obsolete keys (protocol, host, port, path)
into new 'uri' key.
Usage::

    python3 -m vcr.migration PATH

The PATH can be path to the directory with cassettes or cassette itself
"""

import json
import os
import shutil
import sys
import tempfile

import yaml

from . import request
from .serialize import serialize
from .serializers import jsonserializer, yamlserializer
from .stubs.compat import get_httpmessage

# Use the libYAML versions if possible
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def preprocess_yaml(cassette):
    # this is the hack that makes the whole thing work.  The old version used
    # to deserialize to Request objects automatically using pyYaml's !!python
    # tag system.  This made it difficult to deserialize old cassettes on new
    # versions.  So this just strips the tags before deserializing.

    pass


PARTS = ["protocol", "host", "port", "path"]


def build_uri(**parts):
    pass


def _migrate(data):
    pass


def migrate_json(in_fp, out_fp):
    pass


def _list_of_tuples_to_dict(fs):
    pass


def _already_migrated(data):
    pass


def migrate_yml(in_fp, out_fp):
    pass


def migrate(file_path, migration_fn):
    # because we assume that original files can be reverted
    # we will try to copy the content. (os.rename not needed)
    with tempfile.TemporaryFile(mode="w+") as out_fp:
        with open(file_path) as in_fp:
            if not migration_fn(in_fp, out_fp):
                return False
        with open(file_path, "w") as in_fp:
            out_fp.seek(0)
            shutil.copyfileobj(out_fp, in_fp)
        return True


def try_migrate(path):
    if path.endswith(".json"):
        return migrate(path, migrate_json)
    elif path.endswith((".yaml", ".yml")):
        return migrate(path, migrate_yml)
    return False


def main():
    if len(sys.argv) != 2:
        raise SystemExit(
            "Please provide path to cassettes directory or file. Usage: python3 -m vcr.migration PATH",
        )

    path = sys.argv[1]
    if not os.path.isabs(path):
        path = os.path.abspath(path)
    files = [path]
    if os.path.isdir(path):
        files = (os.path.join(root, name) for (root, dirs, files) in os.walk(path) for name in files)
    for file_path in files:
        migrated = try_migrate(file_path)
        status = "OK" if migrated else "FAIL"
        sys.stderr.write(f"[{status}] {file_path}\n")
    sys.stderr.write("Done.\n")


if __name__ == "__main__":
    main()
