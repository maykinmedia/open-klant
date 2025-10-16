from opentelemetry import metrics

meter = metrics.get_meter("openklant.components.klantinteracties")

# klantcontacten
klantcontacten_create_counter = meter.create_counter(
    "openklant.klantcontact.creates",
    description="Amount of klantcontacten created (via the API).",
    unit="1",
)
klantcontacten_update_counter = meter.create_counter(
    "openklant.klantcontact.updates",
    description="Amount of klantcontacten updated (via the API).",
    unit="1",
)
klantcontacten_delete_counter = meter.create_counter(
    "openklant.klantcontact.deletes",
    description="Amount of klantcontacten deleted (via the API).",
    unit="1",
)

# betrokkenen
betrokkenen_create_counter = meter.create_counter(
    "openklant.betrokkene.creates",
    description="Amount of betrokkenen created (via the API).",
    unit="1",
)
betrokkenen_update_counter = meter.create_counter(
    "openklant.betrokkene.updates",
    description="Amount of betrokkenen updated (via the API).",
    unit="1",
)
betrokkenen_delete_counter = meter.create_counter(
    "openklant.betrokkene.deletes",
    description="Amount of betrokkenen deleted (via the API).",
    unit="1",
)

# partijen
partijen_create_counter = meter.create_counter(
    "openklant.partij.creates",
    description="Amount of partijen created (via the API).",
    unit="1",
)
partijen_update_counter = meter.create_counter(
    "openklant.partij.updates",
    description="Amount of partijen updated (via the API).",
    unit="1",
)
partijen_delete_counter = meter.create_counter(
    "openklant.partij.deletes",
    description="Amount of partijen deleted (via the API).",
    unit="1",
)

# actoren
actoren_create_counter = meter.create_counter(
    "openklant.actor.creates",
    description="Amount of actoren created (via the API).",
    unit="1",
)
actoren_update_counter = meter.create_counter(
    "openklant.actor.updates",
    description="Amount of actoren updated (via the API).",
    unit="1",
)
actoren_delete_counter = meter.create_counter(
    "openklant.actor.deletes",
    description="Amount of actoren deleted (via the API).",
    unit="1",
)

# digitale_adressen
digitale_adressen_create_counter = meter.create_counter(
    "openklant.digitaal_adres.creates",
    description="Amount of digitale_adressen created (via the API).",
    unit="1",
)
digitale_adressen_update_counter = meter.create_counter(
    "openklant.digitaal_adres.updates",
    description="Amount of digitale_adressen updated (via the API).",
    unit="1",
)
digitale_adressen_delete_counter = meter.create_counter(
    "openklant.digitaal_adres.deletes",
    description="Amount of digitale_adressen deleted (via the API).",
    unit="1",
)

# interne_taken
interne_taken_create_counter = meter.create_counter(
    "openklant.interne_taak.creates",
    description="Amount of interne_taken created (via the API).",
    unit="1",
)
interne_taken_update_counter = meter.create_counter(
    "openklant.interne_taak.updates",
    description="Amount of interne_taken updated (via the API).",
    unit="1",
)
interne_taken_delete_counter = meter.create_counter(
    "openklant.interne_taak.deletes",
    description="Amount of interne_taken deleted (via the API).",
    unit="1",
)
