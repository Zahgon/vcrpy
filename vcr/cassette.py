import collections
import contextlib
import copy
import inspect
import logging
from inspect import iscoroutinefunction

import wrapt

from ._handle_coroutine import handle_coroutine
from .errors import UnhandledHTTPRequestError
from .matchers import get_matchers_results, method, requests_match, uri
from .patch import CassettePatcherBuilder
from .persisters.filesystem import CassetteDecodeError, CassetteNotFoundError, FilesystemPersister
from .record_mode import RecordMode
from .serializers import yamlserializer
from .util import partition_dict

log = logging.getLogger(__name__)


class CassetteContextDecorator:
    """Context manager/decorator that handles installing the cassette and
    removing cassettes.

    This class defers the creation of a new cassette instance until
    the point at which it is installed by context manager or
    decorator. The fact that a new cassette is used with each
    application prevents the state of any cassette from interfering
    with another.

    Instances of this class are NOT reentrant as context managers.
    However, functions that are decorated by
    ``CassetteContextDecorator`` instances ARE reentrant. See the
    implementation of ``__call__`` on this class for more details.
    There is also a guard against attempts to reenter instances of
    this class as a context manager in ``__exit__``.
    """

    _non_cassette_arguments = (
        "path_transformer",
        "func_path_generator",
        "record_on_exception",
    )

    @classmethod
    def from_args(cls, cassette_class, **kwargs):
        return cls(cassette_class, lambda: dict(kwargs))

    def __init__(self, cls, args_getter):
        self.cls = cls
        self._args_getter = args_getter
        self.__finish = None
        self.__cassette = None

    def _patch_generator(self, cassette):
        pass

    def __enter__(self):
        # This assertion is here to prevent the dangerous behavior
        # that would result from forgetting about a __finish before
        # completing it.
        # How might this condition be met? Here is an example:
        # context_decorator = Cassette.use('whatever')
        # with context_decorator:
        #     with context_decorator:
        #         pass
        assert self.__finish is None, "Cassette already open."
        other_kwargs, cassette_kwargs = partition_dict(
            lambda key, _: key in self._non_cassette_arguments,
            self._args_getter(),
        )
        if other_kwargs.get("path_transformer"):
            transformer = other_kwargs["path_transformer"]
            cassette_kwargs["path"] = transformer(cassette_kwargs["path"])
        self.__cassette = self.cls.load(**cassette_kwargs)
        self.__finish = self._patch_generator(self.__cassette)
        return next(self.__finish)

    def __exit__(self, *exc_info):
        exception_was_raised = any(exc_info)
        record_on_exception = self._args_getter().get("record_on_exception", True)
        if record_on_exception or not exception_was_raised:
            self.__cassette._save()
            self.__cassette = None
        # Fellow programmer, don't remove this `next`, if `self.__finish` is
        # not consumed the unpatcher functions accumulated in the `exit_stack`
        # object created in `_patch_generator` will not be called until
        # `exit_stack` is not garbage collected.
        # This works in CPython but not in Pypy, where the unpatchers will not
        # be called until much later.
        next(self.__finish, None)
        self.__finish = None

    @wrapt.decorator
    def __call__(self, function, instance, args, kwargs):
        # This awkward cloning thing is done to ensure that decorated
        # functions are reentrant. This is required for thread
        # safety and the correct operation of recursive functions.
        args_getter = self._build_args_getter_for_decorator(function)
        return type(self)(self.cls, args_getter)._execute_function(function, args, kwargs)

    def _execute_function(self, function, args, kwargs):
        pass

    def _handle_generator(self, fn):
        """Wraps a generator so that we're inside the cassette context for the
        duration of the generator.
        """
        pass

    def _handle_function(self, fn):
        pass

    @staticmethod
    def get_function_name(function):
        pass

    def _build_args_getter_for_decorator(self, function):
        pass


class Cassette:
    """A container for recorded requests and responses"""

    @classmethod
    def load(cls, **kwargs):
        """Instantiate and load the cassette stored at the specified path."""
        pass

    @classmethod
    def use_arg_getter(cls, arg_getter):
        return CassetteContextDecorator(cls, arg_getter)

    @classmethod
    def use(cls, **kwargs):
        return CassetteContextDecorator.from_args(cls, **kwargs)

    def __init__(
        self,
        path,
        serializer=None,
        persister=None,
        record_mode=RecordMode.ONCE,
        match_on=(uri, method),
        before_record_request=None,
        before_record_response=None,
        custom_patches=(),
        inject=False,
        allow_playback_repeats=False,
        drop_unused_requests=False,
    ):
        self._persister = persister or FilesystemPersister
        self._path = path
        self._serializer = serializer or yamlserializer
        self._match_on = match_on
        self._before_record_request = before_record_request or (lambda x: x)
        log.info(self._before_record_request)
        self._before_record_response = before_record_response or (lambda x: x)
        self.inject = inject
        self.record_mode = record_mode
        self.custom_patches = custom_patches
        self.allow_playback_repeats = allow_playback_repeats
        self.drop_unused_requests = drop_unused_requests

        # self.data is the list of (req, resp) tuples
        self.data = []
        self.play_counts = collections.Counter()
        self.dirty = False
        self.rewound = False

        # Subsets of self.data to store old and played interactions
        self._old_interactions = []
        self._played_interactions = []

    @property
    def play_count(self):
        pass

    @property
    def all_played(self):
        """Returns True if all responses have been played, False otherwise."""
        pass

    @property
    def requests(self):
        pass

    @property
    def responses(self):
        pass

    @property
    def write_protected(self):
        pass

    def append(self, request, response):
        """Add a request, response pair to this cassette"""
        request = self._before_record_request(request)
        if not request:
            return
        log.info("Appending request %s and response %s", request, response)
        # Deepcopy is here because mutation of `response` will corrupt the
        # real response.
        response = copy.deepcopy(response)
        response = self._before_record_response(response)
        if response is None:
            return
        self.data.append((request, response))
        self.dirty = True

    def filter_request(self, request):
        pass

    def _responses(self, request):
        """
        internal API, returns an iterator with all responses matching
        the request.
        """
        pass

    def can_play_response_for(self, request):
        pass

    def play_response(self, request):
        """
        Get the response corresponding to a request, but only if it
        hasn't been played back before, and mark it as played
        """
        pass

    def responses_of(self, request):
        """
        Find the responses corresponding to a request.
        This function isn't actually used by VCR internally, but is
        provided as an external API.
        """
        pass

    def rewind(self):
        pass

    def find_requests_with_most_matches(self, request):
        """
        Get the most similar request(s) stored in the cassette
        of a given request as a list of tuples like this:
        - the request object
        - the successful matchers as string
        - the failed matchers and the related assertion message with the difference details as strings tuple

        This is useful when a request failed to be found,
        we can get the similar request(s) in order to know what have changed in the request parts.
        """
        pass

    def _new_interactions(self):
        """List of new HTTP interactions (request/response tuples)"""
        pass

    def _as_dict(self):
        pass

    def _build_used_interactions_dict(self):
        pass

    def _save(self, force=False):
        pass

    def _load(self):
        pass

    def __str__(self):
        return f"<Cassette containing {len(self)} recorded response(s)>"

    def __len__(self):
        """Return the number of request,response pairs stored in here"""
        return len(self.data)

    def __contains__(self, request):
        """Return whether or not a request has been stored"""
        for index, _ in self._responses(request):
            if self.play_counts[index] == 0 or self.allow_playback_repeats:
                return True
        return False
