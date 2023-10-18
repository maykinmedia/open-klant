"""
Defines the scopes used in the CMC component.
"""

from vng_api_common.scopes import Scope

SCOPE_CONTACTMOMENTEN_ALLES_VERWIJDEREN = Scope(
    "contactmomenten.verwijderen",
    description="""
**Laat toe om**:

* contactmomenten te verwijderen
""",
)

SCOPE_CONTACTMOMENTEN_ALLES_LEZEN = Scope(
    "contactmomenten.lezen",
    description="""
**Laat toe om**:

* contactmomenten te lezen
* contactmomentdetails op te vragen
""",
)

SCOPE_CONTACTMOMENTEN_BIJWERKEN = Scope(
    "contactmomenten.bijwerken",
    description="""
**Laat toe om**:

* attributen van een contactmoment te wijzingen
""",
)

SCOPE_CONTACTMOMENTEN_AANMAKEN = Scope(
    "contactmomenten.aanmaken",
    description="""
**Laat toe om**:

* contactmomenten aan te maken
""",
)
