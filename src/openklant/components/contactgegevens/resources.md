# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Contactgegevens

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/contactgegevens)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| id |  | integer | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| organisaties | De gekoppelde organisaties | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| personen | De gekoppelde personen | array | nee | ~~C~~​R​~~U~~​~~D~~ |
| partijIdentificator | URL-referentie naar de PartijIdentificator (in de Contactgegevens API). | string | ja | C​R​U​D |

## Organisatie

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/organisatie)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| id |  | integer | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| handelsnaam | De naam waaronder een bedrijf of vestiging handelt. | string | ja | C​R​U​D |
| oprichtingsdatum | Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21 | string | nee | C​R​U​D |
| opheffingsdatum | Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21 | string | nee | C​R​U​D |

## Persoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/persoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| id |  | integer | nee | ~~C~~​R​~~U~~​~~D~~ |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| geboortedatum | Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21 | string | ja | C​R​U​D |
| overlijdensdatum | Aanduiding van datum volgens de NEN-ISO 8601:2019-standaard. Een datum wordt genoteerd van het meest naar het minst significante onderdeel. Een voorbeeld: 2022-02-21 | string | nee | C​R​U​D |
| geslachtsnaam | De (geslachts)naam waarvan de eventueel aanwezige voorvoegsels zijn afgesplitst. Gebruik van de wildcard is toegestaan bij invoer van ten minste 3 letters. Zoeken met tekstvelden is case-insensitive. | string | ja | C​R​U​D |
| geslacht | Geeft aan dat de persoon een man of een vrouw is, of dat het geslacht (nog) onbekend is. | string | nee | C​R​U​D |
| voorvoegsel | Deel van de geslachtsnaam dat vooraf gaat aan de rest van de geslachtsnaam. Zoeken met tekstvelden is case-insensitive. | string | nee | C​R​U​D |
| voornamen | De verzameling namen die, gescheiden door spaties, aan de geslachtsnaam voorafgaat. Gebruik van de wildcard is toegestaan. Zoeken met tekstvelden is case-insensitive. | string | nee | C​R​U​D |


* Create, Read, Update, Delete
