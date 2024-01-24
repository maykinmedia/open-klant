from .externe_registers import ExternRegisterViewSet
from .kanalen import KanaalViewSet
from .landen import LandViewSet
from .soorten_digitaal_adres import SoortDigitaalAdresViewSet
from .soorten_object import SoortObjectViewSet
from .soorten_objectid import SoortObjectidViewSet
from .talen import TaalViewSet

__all__ = [
    "ExternRegisterViewSet",
    "KanaalViewSet",
    "LandViewSet",
    "SoortDigitaalAdresViewSet",
    "SoortObjectViewSet",
    "SoortObjectidViewSet",
    "TaalViewSet",
]
