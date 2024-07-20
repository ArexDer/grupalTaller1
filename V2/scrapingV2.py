import requests
import json

# Endpoint de TheNewsApi con token de API
base_url = "https://api.thenewsapi.com/v1/news/top"
api_token = "ce4f59a7b09b465290dc07dbba2fc31e"
locale = "us"
total_news = 100
news_per_request = 15

# Lista para almacenar todas las noticias
all_news = []

# Realizar múltiples solicitudes para obtener el total de noticias necesarias
for i in range(0, total_news, news_per_request):
    params = {
        "api_token": api_token,
        "locale": locale,
        "limit": news_per_request,
        "page": i // news_per_request + 1
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()

        if 'data' in data:
            all_news.extend(data['data'])
        else:
            print("No se encontraron datos en la respuesta.")
    else:
        print(f"Error en la solicitud: {response.status_code}")

# Limitar a 100 noticias si se obtuvieron más
all_news = all_news[:total_news]

# Guardar las noticias en un archivo JSON
with open('news_data.json', 'w') as json_file:
    json.dump(all_news, json_file, indent=4)

print(f"{len(all_news)} noticias guardadas exitosamente en news_data.json")
