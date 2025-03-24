## Notificaties
## Berichtkenmerken voor Open Klant API

Kanalen worden typisch per component gedefinieerd. Producers versturen berichten op bepaalde kanalen,
consumers ontvangen deze. Consumers abonneren zich via een notificatiecomponent (zoals <a href="https://notificaties-api.vng.cloud/api/v1/schema/" rel="nofollow">https://notificaties-api.vng.cloud/api/v1/schema/</a>) op berichten.

Hieronder staan de kanalen beschreven die door deze component gebruikt worden, met de kenmerken bij elk bericht.

De architectuur van de notificaties staat beschreven op <a href="https://github.com/VNG-Realisatie/notificaties-api" rel="nofollow">https://github.com/VNG-Realisatie/notificaties-api</a>.


### internetaken

**Kanaal**
`internetaken`

**Main resource**

`internetaak`



**Kenmerken**

* `nummer`: Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke interne taak aan te duiden.
* `gevraagdeHandeling`: Handeling die moet worden uitgevoerd om de taak af te ronden.
* `toelichting`: Toelichting die, aanvullend bij de inhoud van het klantcontact dat aanleiding gaf tot de taak en de gevraagde handeling, bijdraagt aan het kunnen afhandelen van de taak.
* `status`: Aanduiding van de vordering bij afhandeling van de interne taak.

**Resources en acties**


* <code>internetaak</code>: create, update, destroy


### partijen

**Kanaal**
`partijen`

**Main resource**

`partij`



**Kenmerken**

* `nummer`: Uniek identificerend nummer dat tijdens communicatie tussen mensen kan worden gebruikt om de specifieke partij aan te duiden.
* `interneNotitie`: Mededelingen, aantekeningen of bijzonderheden over de partij, bedoeld voor intern gebruik.
* `soortPartij`: Geeft aan van welke specifieke soort partij sprake is.

**Resources en acties**


* <code>partij</code>: create, update, destroy


