import factory


class KlantContactDataFactory(factory.DictFactory):
    nummer = "7948723947"
    kanaal = "changed"
    onderwerp = "changed"
    inhoud = "changed"
    indicatieContactGelukt = False
    taal = "de"
    vertrouwelijk = False
    plaatsgevondenOp = "2020-08-24T14:15:22Z"


class BezoekAdresDataFactory(factory.DictFactory):
    nummeraanduidingId = "4a282b5c-16d7-401d-9737-28e98c865ab2"
    adresregel1 = "adres1"
    adresregel2 = "adres2"
    adresregel3 = "adres3"
    land = "6030"


class CorrespondentieAdresDataFactory(factory.DictFactory):
    nummeraanduidingId = "c06918d9-899b-4d98-a10d-08436ebc6c20"
    adresregel1 = "adres1"
    adresregel2 = "adres2"
    adresregel3 = "adres3"
    land = "6030"


class ContactNaamDataFactory(factory.DictFactory):
    voorletters = "P"
    voornaam = "Phil"
    voorvoegselAchternaam = ""
    achternaam = "Bozeman"


class BetrokkeneDataFactory(factory.DictFactory):
    wasPartij = None
    bezoekadres = factory.SubFactory(BezoekAdresDataFactory)
    correspondentieadres = factory.SubFactory(CorrespondentieAdresDataFactory)
    contactnaam = factory.SubFactory(ContactNaamDataFactory)
    rol = "vertegenwoordiger"
    organisatienaam = "Whitechapel"
    initiator = True


class OnderwerpObjectIdentificatorDataFactory(factory.DictFactory):
    codeObjecttype = "codeObjecttype"
    codeSoortObjectId = "codeSoortObjectId"
    objectId = "objectId"
    codeRegister = "codeRegister"


class OnderwerpObjectDataFactory(factory.DictFactory):
    wasKlantcontact = None
    onderwerpobjectidentificator = factory.SubFactory(
        OnderwerpObjectIdentificatorDataFactory
    )
