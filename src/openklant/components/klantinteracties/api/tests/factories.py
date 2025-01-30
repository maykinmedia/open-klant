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
    nummeraanduidingId = "1234567890000001"
    adresregel1 = "adres1"
    adresregel2 = "adres2"
    adresregel3 = "adres3"
    land = "NL"


class CorrespondentieAdresDataFactory(factory.DictFactory):
    nummeraanduidingId = "1234567890000002"
    adresregel1 = "adres1"
    adresregel2 = "adres2"
    adresregel3 = "adres3"
    land = "NL"


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
