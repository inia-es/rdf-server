# coding=utf-8
from ckan2rdf import CkanMetadata
import json

metadata = CkanMetadata("lens")

json_object = {
    "name":"lens-colecciones-crf",
    "title":"Lens Colecciones CRF",
    "idiomatitulo1":"espanoltitulo1",
    "title2":"Lens Collections CRF",
    "idiomatitulo2":"inglestitulo2",
    "notes":"Datos de pasaporte de las colecciones de lens del CERF (Centro de Recursos Fitogenéticos), "\
    "dentro de esta colección se encuentran diferentes especies de lens",
    "autores":["Test1", "Test2"],
    "subfield_email":["test1@inia.es","test2@inia.es"],
    "subfield_orcid":["http://orcid.org/0000-0002-6787-0866"],
    "contacto":"Test3",
    "contacto_email":"test3@inia.es"
}

print metadata.transformToRdf(json_object)