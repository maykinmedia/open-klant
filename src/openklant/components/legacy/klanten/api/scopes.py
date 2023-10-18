"""
Defines the scopes used in the CMC component.
"""

from vng_api_common.scopes import Scope

SCOPE_KLANTEN_ALLES_VERWIJDEREN = Scope(
    "klanten.verwijderen",
    description="""
**Laat toe om**:

* klanten te verwijderen
""",
)

SCOPE_KLANTEN_ALLES_LEZEN = Scope(
    "klanten.lezen",
    description="""
**Laat toe om**:

* klanten te lezen
* klantdetails op te vragen
""",
)

SCOPE_KLANTEN_BIJWERKEN = Scope(
    "klanten.bijwerken",
    description="""
**Laat toe om**:

* attributen van een klant te wijzingen
""",
)

SCOPE_KLANTEN_AANMAKEN = Scope(
    "klanten.aanmaken",
    description="""
**Laat toe om**:

* klanten aan te maken
""",
)
