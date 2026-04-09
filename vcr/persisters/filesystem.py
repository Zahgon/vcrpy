# .. _persister_example:

from pathlib import Path

from ..serialize import deserialize, serialize


class CassetteNotFoundError(FileNotFoundError):
    pass


class CassetteDecodeError(ValueError):
    pass


class FilesystemPersister:
    @classmethod
    def load_cassette(cls, cassette_path, serializer):
        pass

    @staticmethod
    def save_cassette(cassette_path, cassette_dict, serializer):
        pass
