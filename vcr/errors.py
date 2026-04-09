class CannotOverwriteExistingCassetteException(Exception):
    def __init__(self, *args, **kwargs):
        self.cassette = kwargs["cassette"]
        self.failed_request = kwargs["failed_request"]
        message = self._get_message(kwargs["cassette"], kwargs["failed_request"])
        super().__init__(message)

    @staticmethod
    def _get_message(cassette, failed_request):
        """Get the final message related to the exception"""
        pass


class UnhandledHTTPRequestError(KeyError):
    """Raised when a cassette does not contain the request we want."""
