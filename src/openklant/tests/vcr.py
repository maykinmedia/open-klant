import os
from pathlib import Path

from maykin_common.vcr import VCRMixin as _VCRMixin

RECORD_MODE = os.environ.get("VCR_RECORD_MODE", "none")


class VCRMixin(_VCRMixin):
    """
    Mixin to use VCR in your unit tests.

    Using this mixin will result in HTTP requests/responses being recorded.
    """

    VCR_TEST_FILES: Path
    """
    A :class:`pathlib.Path` instance where the cassettes should be stored.
    """

    def _get_cassette_library_dir(self):
        assert self.VCR_TEST_FILES, (
            "You must define the `VCR_TEST_FILES` class attribute"
        )
        return str(self.VCR_TEST_FILES / "vcr_cassettes" / self.__class__.__qualname__)

    def _get_vcr_kwargs(self, **kwargs) -> dict:
        kwargs = super()._get_vcr_kwargs()
        kwargs.setdefault("record_mode", RECORD_MODE)
        return kwargs
