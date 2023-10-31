from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from openklant.components.klantinteracties.api.serializers.actoren import (
    ActorSerializer,
    GeautomatiseerdeActorSerializer,
    MedewerkerSerializer,
    OrganisatorischeEenheidSerializer,
)
from openklant.components.klantinteracties.models.actoren import (
    Actor,
    GeautomatiseerdeActor,
    Medewerker,
    OrganisatorischeEenheid,
)


class ActorViewSet(viewsets.ModelViewSet):
    """
    Iets dat of iemand die voor de gemeente werkzaamheden uitvoert.

    create:
    Maak een actor aan.

    Maak een actor aan.

    list:
    Alle actoren opvragen.

    Alle actoren opvragen.

    retrieve:
    Een specifiek actor opvragen.

    Een specifiek actor opvragen.

    update:
    Werk een actor in zijn geheel bij.

    Werk een actor in zijn geheel bij.

    partial_update:
    Werk een actor deels bij.

    Werk een actor deels bij.

    destroy:
    Verwijder een actor.

    Verwijder een actor.
    """

    queryset = Actor.objects.order_by("-pk")
    serializer_class = ActorSerializer
    lookup_field = "uuid"
    pagination_class = PageNumberPagination


class GeautomatiseerdeActorViewSet(viewsets.ModelViewSet):
    """
    Functie van de geautomatiseerde actor of beschrijving van de werkzaamheden die deze uitvoert.

    create:
    Maak een geautomatiseerde actor aan.

    Maak een geautomatiseerde actor aan.

    list:
    Alle geautomatiseerde actoren opvragen.

    Alle geautomatiseerde actoren opvragen.

    retrieve:
    Een specifiek geautomatiseerde actor opvragen.

    Een specifiek geautomatiseerde actor opvragen.

    update:
    Werk een geautomatiseerde actor in zijn geheel bij.

    Werk een geautomatiseerde actor in zijn geheel bij.

    partial_update:
    Werk een geautomatiseerde actor deels bij.

    Werk een geautomatiseerde actor deels bij.

    destroy:
    Verwijder een geautomatiseerde actor.

    Verwijder een geautomatiseerde actor.
    """

    queryset = GeautomatiseerdeActor.objects.order_by("-pk")
    serializer_class = GeautomatiseerdeActorSerializer
    lookup_field = "id"
    pagination_class = PageNumberPagination


class MedewerkerViewSet(viewsets.ModelViewSet):
    """
    Een MEDEWERKER van de organisatie die zaken behandelt uit hoofde van zijn of
    haar functie binnen een ORGANISATORISCHE EENHEID.

    create:
    Maak een medewerker aan.

    Maak een medewerker aan.

    list:
    Alle medewerkers opvragen.

    Alle medewerkers opvragen.

    retrieve:
    Een specifiek medewerker opvragen.

    Een specifiek medewerker opvragen.

    update:
    Werk een medewerker in zijn geheel bij.

    Werk een medewerker in zijn geheel bij.

    partial_update:
    Werk een medewerker deels bij.

    Werk een medewerker deels bij.

    destroy:
    Verwijder een medewerker.

    Verwijder een medewerker.
    """

    queryset = Medewerker.objects.order_by("-pk")
    serializer_class = MedewerkerSerializer
    lookup_field = "id"
    pagination_class = PageNumberPagination


class OrganisatorischeEenheidViewSet(viewsets.ModelViewSet):
    """
    Het deel van een functioneel afgebakend onderdeel binnen de organisatie dat
    haar activiteiten uitvoert binnen een VESTIGING VAN ZAAKBEHANDELENDE ORGANISATIE
    en die verantwoordelijk is voor de behandeling van zaken.

    create:
    Maak een organisatorische eenheid aan.

    Maak een organisatorische eenheid aan.

    list:
    Alle organisatorische eenheid opvragen.

    Alle organisatorische eenheid opvragen.

    retrieve:
    Een specifiek organisatorische eenheid opvragen.

    Een specifiek organisatorische eenheid opvragen.

    update:
    Werk een organisatorische eenheid in zijn geheel bij.

    Werk een organisatorische eenheid in zijn geheel bij.

    partial_update:
    Werk een organisatorische eenheid deels bij.

    Werk een organisatorische eenheid deels bij.

    destroy:
    Verwijder een organisatorische eenheid.

    Verwijder een organisatorische eenheid.
    """

    queryset = OrganisatorischeEenheid.objects.order_by("-pk")
    serializer_class = OrganisatorischeEenheidSerializer
    lookup_field = "id"
    pagination_class = PageNumberPagination
