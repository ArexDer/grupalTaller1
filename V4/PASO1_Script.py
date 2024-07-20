from eventregistry import *

# Configura el cliente de Event Registry
#https://newsapi.ai/dashboard?tab=home
er = EventRegistry(apiKey="f6dd4cbe-e06c-4a09-bdd0-d9dbcd5d8dad", allowUseOfArchive=False)

# Obtiene los URIs para las empresas y la categoría
microsoftUri = er.getConceptUri("Linux")
googleUri = er.getConceptUri("Windows")
#businessUri = er.getCategoryUri("news business")

# Configura la consulta de artículos
q = QueryArticlesIter(
    conceptUri=QueryItems.OR([microsoftUri, googleUri]),
    #categoryUri=businessUri
)

# Abre un archivo para escribir los resultados
filename = "v4/articlesSistemas.txt"
with open(filename, 'w', encoding='utf-8') as file:
    # Obtén como máximo 500 artículos más recientes
    for art in q.execQuery(er, sortBy="date", maxItems=500):
        # Escribe cada artículo en el archivo
        file.write(str(art) + '\n')
        # También podrías guardar campos específicos como art['title'], art['body'], etc.

print(f"Se han guardado los artículos en {filename}")
