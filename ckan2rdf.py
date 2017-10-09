from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import OWL, DCTERMS, RDF, FOAF, RDFS, SKOS, XSD

class CkanMetadata:

    def __init__(self,dataset_name):

        self.g = Graph()
        # Configuration of namespaces
        self.inia = Namespace("https://w3id.org/def/inia#")
        self.g.bind("inia", self.inia)

        self.cc = Namespace("http://creativecommons.org/ns#")
        self.g.bind("cc", self.cc)

        self.dataid = Namespace("http://dataid.dbpedia.org/ns/core#")
        self.g.bind("dataid", self.dataid)

        self.dwc = Namespace("http://rs.tdwg.org/dwc/terms/")
        self.g.bind("dwc", self.dwc)

        self.ext = Namespace("http://def.seegrid.csiro.au/isotc211/iso19115/2003/extent#")
        self.g.bind("ext", self.ext)

        self.lvont = Namespace("http://lexvo.org/ontology#")
        self.g.bind("lvont", self.lvont)

        self.odrl = Namespace("http://www.w3c.org/ns/odrl/2/")
        self.g.bind("odrl", self.odrl)

        self.time = Namespace("http://www.w3c.org/2006/time#")
        self.g.bind("time", self.time)

        self.vann = Namespace("http://purl.org/vocab/vann/")
        self.g.bind("vann", self.vann)

        self.voaf = Namespace("http://purl.org/vocommons/voaf#")
        self.g.bind("voaf", self.voaf)

        self.g.bind("dcterms", DCTERMS)
        self.g.bind("owl", OWL)
        self.g.bind("foaf", FOAF)
        self.g.bind("rdf", RDF)
        self.g.bind("rdfs", RDFS)
        self.g.bind("skos", SKOS)
        self.g.bind("xsd", XSD)

    def transformToRdf (self,metadata):

        initial_node = BNode()

        d_title = URIRef(BNode(metadata['name']))

        title = Literal(metadata["title"])
        self.g.add((d_title,RDF['type'],OWL['NamedIndividual']))
        self.g.add((d_title, RDF['type'], self.inia.Dataset))
        self.g.add((d_title, DCTERMS['title'], title))

        #idiomatitulo1 = metadata["idiomatitulo1"]
        #if (idiomatitulo1 == "espanoltitulo1"):
         #   self.g.add((title, DCTERMS["language"],self.lvont.es))

        title2 = Literal(metadata["title2"])
        self.g.add((d_title, DCTERMS['title'], title2))

        d_description = URIRef(BNode(metadata['name']))
        description = Literal(metadata["notes"])
        self.g.add((d_description,DCTERMS['description'],description))

        d_author = URIRef(BNode(metadata['name']))

        authors = metadata["autores"]

        for i in range(0,len(authors)):

            person = "person"+str((i+1))
            personal_identifier = "personalIdentifier"+str((i+1))
            d_person = URIRef(BNode(person))

            orcid_identifiers = metadata["subfield_orcid"]
            emails = metadata["subfield_email"]

            if i < len(orcid_identifiers) and orcid_identifiers[i]!="":
                d_person_identifier = URIRef(BNode(personal_identifier))
                orcid = Literal(orcid_identifiers[i])

                self.g.add((d_person_identifier, RDF['type'],OWL['NamedIndividual']))
                self.g.add((d_person_identifier, RDF['type'], URIRef("http://purl.org/spar/datacite/PersonalIdentifier")))
                self.g.add((d_person_identifier, URIRef("http://purl.org/spar/datacite/usesIdentifierScheme"),URIRef("http://purl.org/spar/datacite/orcid")))
                self.g.add((d_person_identifier, URIRef("http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue"), orcid))
                self.g.add((d_person,URIRef("http://purl.org/spar/datacite/hasIdentifier"),d_person_identifier))


            self.g.add((d_person,RDF['type'],OWL['NamedIndividual']))
            self.g.add((d_person, RDF['type'],FOAF['Person']))
            self.g.add((d_person, FOAF['mbox'], Literal(emails[i])))
            self.g.add((d_person, FOAF['name'], Literal(authors[i])))

            self.g.add((d_author, DCTERMS['creator'], d_person))

        d_contact = URIRef(BNode('contact'))
        self.g.add((d_contact, RDF['type'],OWL['NamedIndividual']))
        self.g.add((d_contact, RDF['type'],FOAF['Person']))
        self.g.add((d_contact,FOAF['name'],Literal(metadata['contacto'])))
        self.g.add((d_contact, FOAF['mbox'], URIRef(metadata['contacto_email'])))

        self.g.add((d_title, self.inia['contactPerson'], d_contact))

        return self.g.serialize(format='turtle')