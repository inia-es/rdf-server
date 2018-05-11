from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import OWL, DCTERMS, RDF, FOAF, RDFS, SKOS, XSD
import re

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

        self.datacite = Namespace("http://purl.org/spar/datacite/")
        self.g.bind("datacite", self.datacite)

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

        self.ext = Namespace("http://def.seedgrid.csiro.au/isotc211/iso19115/2003/extend#")
        self.g.bind("ext", self.ext)

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
        self.g.add((d_title, RDF['type'], OWL['NamedIndividual']))
        self.g.add((d_title, RDF['type'], self.inia.Dataset))
        self.g.add((d_title, DCTERMS['title'], title))

        # idiomatitulo1 = metadata["idiomatitulo1"]
        # if (idiomatitulo1 == "espanoltitulo1"):
        #   self.g.add((title, DCTERMS["language"],self.lvont.es))

        title2 = Literal(metadata["title2"])
        self.g.add((d_title, DCTERMS['title'], title2))

        d_description = URIRef(BNode(metadata['name']))
        description = Literal(metadata["notes"])
        self.g.add((d_description, DCTERMS['description'], description))

        d_author = URIRef(BNode(metadata['name']))

        authors = re.findall(r'"\s*([^"]*?)\s*"', metadata["autores"])

        for i in range(0, len(authors)):

            person = "person" + str((i + 1))
            personal_identifier = "personalIdentifier" + str((i + 1))
            d_person = URIRef(BNode(person))

            orcid_identifiers = metadata["subfield_orcid"]
            emails = metadata["subfield_email"]

            if i < len(orcid_identifiers) and orcid_identifiers[i] != "":
                d_person_identifier = URIRef(BNode(personal_identifier))
                orcid = Literal(orcid_identifiers[i])

                self.g.add((d_person_identifier, RDF['type'], OWL['NamedIndividual']))
                self.g.add(
                    (d_person_identifier, RDF['type'], URIRef("http://purl.org/spar/datacite/PersonalIdentifier")))
                self.g.add((d_person_identifier, URIRef("http://purl.org/spar/datacite/usesIdentifierScheme"),
                            URIRef("http://purl.org/spar/datacite/orcid")))
                self.g.add((d_person_identifier,
                            URIRef("http://www.essepuntato.it/2010/06/literalreification/hasLiteralValue"), orcid))
                self.g.add((d_person, URIRef("http://purl.org/spar/datacite/hasIdentifier"), d_person_identifier))

            self.g.add((d_person, RDF['type'], OWL['NamedIndividual']))
            self.g.add((d_person, RDF['type'], FOAF['Person']))
            if i < len(emails):
                self.g.add((d_person, FOAF['mbox'], Literal(emails[i])))
            self.g.add((d_person, FOAF['name'], Literal(authors[i])))

            self.g.add((d_author, DCTERMS['creator'], d_person))


        d_contact = URIRef(BNode('contact'))
        self.g.add((d_contact, RDF['type'], OWL['NamedIndividual']))
        self.g.add((d_contact, RDF['type'], FOAF['Person']))
        self.g.add((d_contact, FOAF['name'], Literal(metadata['contacto'])))
        self.g.add((d_contact, FOAF['mbox'], URIRef(metadata['contacto_email'])))

        self.g.add((d_title, self.inia['contactPerson'], d_contact))

        ##Missing collaborators

        if metadata['organismo'] != '':
            self.g.add((d_title, DCTERMS['publisher'], Literal(metadata['organismo'])))

        if metadata['fechapublicaion'] != '':
            self.g.add((d_title, DCTERMS['issued'], Literal(metadata['fechapublicaion'])))

        # Missing tags

        if metadata['doi'] != '':
            self.g.add((d_title, self.datacite['hasIdentifier'], URIRef(metadata['doi'])))

        # Missing tematic

        # Project
        if metadata['nombre_proyecto'] != '':
            d_project = URIRef(BNode(metadata['nombre_proyecto']))

            self.g.add((d_project, FOAF['name'], Literal(metadata['nombre_proyecto'])))
            self.g.add((d_project, self.inia['name'], Literal(metadata['codigoproyecto_proyecto'])))
            self.g.add((d_project, self.inia['fundedBy'], Literal(metadata['entefinanciador_proyecto'])))
            self.g.add((d_project, FOAF['homepage'], URIRef(metadata['webfinanciador_proyecto'])))

            self.g.add((d_title, self.inia['developedWithinProject'], d_project))

        #Ambito Temporal

        if "fechainicio_ambitotemporal" in metadata:
            if metadata['fechainicio_ambitotemporal'] != '':
                self.g.add((d_title, self.inia['startingDate'], Literal(metadata['fechainicio_ambitotemporal'])))

        if "fechafinal_ambitotemporal" in metadata:
            if metadata['fechafinal_ambitotemporal'] != '':
                self.g.add((d_title, self.inia['finalDate'], Literal(metadata['fechafinal_ambitotemporal'])))

        if "descripcion_ambitotemporal" in metadata:
            if metadata['descripcion_ambitotemporal'] != '':
                self.g.add((d_title, self.inia['temporalScope'], Literal(metadata['descripcion_ambitotemporal'])))

        #Ambito geografico

        if "texto_ambitogeografico" in metadata:
            if metadata['texto_ambitogeografico'] != '':
                self.g.add((d_title, self.inia['spatialScope'], Literal(metadata['texto_ambitogeografico']) ))

        d_geospatial = URIRef(BNode('geospatial'))

        if "latitudizq_ambitogeografico" in metadata:
            if metadata['latitudizq_ambitogeografico'] != '':
                self.g.add((d_geospatial, self.ext['northBoundLatitude'], Literal(metadata['ext:northBoundLatitude'])))

        if "longitudizq_ambitogeografico" in metadata:
            if metadata['longitudizq_ambitogeografico'] != '':
                self.g.add((d_geospatial, self.ext['westBoundLongitude'], Literal(metadata['longitudizq_ambitogeografico'])))

        if "latituddcha_ambitogeografico" in metadata:
            if metadata['latituddcha_ambitogeografico'] != '':
                self.g.add((d_geospatial, self.ext['southBoundLatitude'], Literal(metadata['latituddcha_ambitogeografico'])))


        if "longituddcha_ambitogeografico" in metadata:
            if metadata['longituddcha_ambitogeografico'] != '':
                self.g.add((d_geospatial, self.ext['eastBoundLongitude'], Literal(metadata['longituddcha_ambitogeografico'])))

        self.g.add((d_title, DCTERMS['spatial'], d_geospatial))

        if "politicas_de_uso" in metadata:
            if metadata['politicas_de_uso'] != '':
                self.g.add((d_title, DCTERMS['rights'], Literal(metadata['politicas_de_uso'])))

        if "politica_uso_uri" in metadata:
            if metadata['politica_uso_uri'] != '':
                self.g.add((d_title, DCTERMS['license'], Literal(metadata['politica_uso_uri'])))

        if "terminos_uso" in metadata:
            if metadata['terminos_uso'] != '':
                self.g.add((d_title, self.dataid['openness'], Literal(metadata['terminos_uso'])))

        if "licencia_abierta" in metadata:
            if metadata['licencia_abierta'] != '':
                self.g.add((d_title, self.dataid['openness'], Literal(metadata['licencia_abierta'])))


        #relations_name = re.findall(r'"\s*([^"]*?)\s*"', metadata["relaciones"])
        #relations_tipo = re.findall(r'"\s*([^"]*?)\s*"', metadata["subfield_tipo_relacion"])

        #for i in range(0, len(relations_name)):
         #   d_relation = URIRef(BNode(relations_name[i]))

        if "fecha_embargo" in metadata:
            if metadata['fecha_embargo'] != '':
                self.g.add((d_title, self.inia['embargoDate'], Literal(metadata('fecha_embargo'))))

        if "cita" in metadata:
            if metadata['cita'] != '':
                self.g.add((d_title, self.inia['isCiteBy'], Literal(metadata('cita'))))

        if "instrumedida" in metadata:
            if metadata['instrumedida'] != '':
                self.g.add((d_title, self.inia['equipment'], Literal(metadata('instrumedida'))))

        if "numelementos" in metadata:
            if metadata['numelementos'] != '':
                self.g.add((d_title, self.inia['elementsNumber'], Literal(metadata['numelementos'])))

        if "softrelacionado" in metadata:
            if metadata['softrelacionado'] != '':
                self.g.add((d_title, self.inia['software'], Literal(metadata['softrelacionado'])))

        return self.g.serialize(format='turtle')