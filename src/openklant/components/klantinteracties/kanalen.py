from openklant.components.klantinteracties.models.internetaken import InterneTaak
from openklant.components.klantinteracties.models.partijen import Partij
from openklant.utils.kanaal import Kanaal

KANAAL_PARTIJ = Kanaal(
    "partijen",
    main_resource=Partij,
    kenmerken=(
        "nummer",
        "interne_notitie",
        "soort_partij",
    ),
)

KANAAL_INTERNETAAK = Kanaal(
    "internetaken",
    main_resource=InterneTaak,
    kenmerken=(
        "nummer",
        "gevraagde_handeling",
        "toelichting",
        "status",
        "klantcontact.uuid",
    ),
)
