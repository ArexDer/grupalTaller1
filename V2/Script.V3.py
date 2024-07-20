from eventregistry import *

# Configura el cliente de Event Registry
er = EventRegistry(apiKey="7f3e1d23-cead-4c5b-8a7b-5e47da1e9586", allowUseOfArchive=False)

# Obtiene los URIs para las empresas y la categoría
microsoftUri = er.getConceptUri("Euro Copa")
googleUri = er.getConceptUri("Copa America")
#businessUri = er.getCategoryUri("news business")

# Configura la consulta de artículos
q = QueryArticlesIter(
    conceptUri=QueryItems.OR([microsoftUri, googleUri]),
    #categoryUri=businessUri
)

# Abre un archivo para escribir los resultados
filename = "articlesSport.txt"
with open(filename, 'w', encoding='utf-8') as file:
    # Obtén como máximo 500 artículos más recientes
    for art in q.execQuery(er, sortBy="date", maxItems=500):
        # Escribe cada artículo en el archivo
        file.write(str(art) + '\n')
        # También podrías guardar campos específicos como art['title'], art['body'], etc.

print(f"Se han guardado los artículos en {filename}")
