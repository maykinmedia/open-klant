# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Organisatie

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/organisatie)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| id |  | integer | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| contactgegevens | De contact gegevens van de huidige organisatie | string | ja | C​R​U​D |
| handelsnaam | De naam waaronder een bedrijf of vestiging handelt. | string | ja | C​R​U​D |
| oprichtingsdatum | Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21 | string | nee | C​R​U​D |
| opheffingsdatum | Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21 | string | nee | C​R​U​D |


* Create, Read, Update, Delete
