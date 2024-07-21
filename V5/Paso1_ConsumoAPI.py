from eventregistry import *
import json

# Configura el cliente de Event Registry
er = EventRegistry(apiKey="7f3e1d23-cead-4c5b-8a7b-5e47da1e9586", allowUseOfArchive=False)

# Obtiene los URIs para las empresas y la categoría
microsoftUri = er.getConceptUri("Linux")
googleUri = er.getConceptUri("Windows")

# Configura la consulta de artículos
q = QueryArticlesIter(
    conceptUri=QueryItems.OR([microsoftUri, googleUri]),
)

# Obtén como máximo 500 artículos más recientes
articles = []
for art in q.execQuery(er, sortBy="date", maxItems=500):
    # Guarda campos específicos del artículo
    articles.append({
        "title": art.get("title"),
        "body": art.get("body"),
        "date": art.get("date"),
        "url": art.get("url")
    })

# Guarda los artículos en un archivo JSON
filename = "articlesSistemas.json"
with open(filename, 'w', encoding='utf-8') as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)

print(f"Se han guardado los artículos en {filename}")
