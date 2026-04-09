import inspect
import os
import unittest

from .config import VCR


class VCRMixin:
    """A TestCase mixin that provides VCR integration."""

    vcr_enabled = True

    def setUp(self):
        pass

    def _get_vcr(self, **kwargs):
        pass

    def _get_vcr_kwargs(self, **kwargs):
        pass

    def _get_cassette_library_dir(self):
        pass

    def _get_cassette_name(self):
        pass


class VCRTestCase(VCRMixin, unittest.TestCase):
    pass
