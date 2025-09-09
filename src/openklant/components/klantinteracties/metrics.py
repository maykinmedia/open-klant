from opentelemetry import metrics

meter = metrics.get_meter("openklant.components.klantinteracties")

# klantcontacten
klantcontacten_create_counter = meter.create_counter(
    "klantcontacten.create",
    description="Amount of klantcontacten created (via the API).",
    unit="1",
)
klantcontacten_update_counter = meter.create_counter(
    "klantcontacten.update",
    description="Amount of klantcontacten updated (via the API).",
    unit="1",
)
klantcontacten_delete_counter = meter.create_counter(
    "klantcontacten.delete",
    description="Amount of klantcontacten deleted (via the API).",
    unit="1",
)

# betrokkenen
betrokkenen_create_counter = meter.create_counter(
    "betrokkenen.create",
    description="Amount of betrokkenen created (via the API).",
    unit="1",
)
betrokkenen_update_counter = meter.create_counter(
    "betrokkenen.update",
    description="Amount of betrokkenen updated (via the API).",
    unit="1",
)
betrokkenen_delete_counter = meter.create_counter(
    "betrokkenen.delete",
    description="Amount of betrokkenen deleted (via the API).",
    unit="1",
)

# partijen
partijen_create_counter = meter.create_counter(
    "partijen.create",
    description="Amount of partijen created (via the API).",
    unit="1",
)
partijen_update_counter = meter.create_counter(
    "partijen.update",
    description="Amount of partijen updated (via the API).",
    unit="1",
)
partijen_delete_counter = meter.create_counter(
    "partijen.delete",
    description="Amount of partijen deleted (via the API).",
    unit="1",
)

# actoren
actoren_create_counter = meter.create_counter(
    "actoren.create",
    description="Amount of actoren created (via the API).",
    unit="1",
)
actoren_update_counter = meter.create_counter(
    "actoren.update",
    description="Amount of actoren updated (via the API).",
    unit="1",
)
actoren_delete_counter = meter.create_counter(
    "actoren.delete",
    description="Amount of actoren deleted (via the API).",
    unit="1",
)

# digitale_adressen
digitale_adressen_create_counter = meter.create_counter(
    "digitale_adressen.create",
    description="Amount of digitale_adressen created (via the API).",
    unit="1",
)
digitale_adressen_update_counter = meter.create_counter(
    "digitale_adressen.update",
    description="Amount of digitale_adressen updated (via the API).",
    unit="1",
)
digitale_adressen_delete_counter = meter.create_counter(
    "digitale_adressen.delete",
    description="Amount of digitale_adressen deleted (via the API).",
    unit="1",
)

# interne_taken
interne_taken_create_counter = meter.create_counter(
    "interne_taken.create",
    description="Amount of interne_taken created (via the API).",
    unit="1",
)
interne_taken_update_counter = meter.create_counter(
    "interne_taken.update",
    description="Amount of interne_taken updated (via the API).",
    unit="1",
)
interne_taken_delete_counter = meter.create_counter(
    "interne_taken.delete",
    description="Amount of interne_taken deleted (via the API).",
    unit="1",
)
