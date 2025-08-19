import inspect
from pathlib import Path
from typing import override

from maykin_common.vcr import VCRMixin as _VCRMixin


class VCRMixin(_VCRMixin):
    @override
    def _get_cassette_library_dir(self):
        class_name = self.__class__.__qualname__
        path = Path(inspect.getfile(self.__class__))
        return str(path.parent / "vcr_cassettes" / path.stem / class_name)
