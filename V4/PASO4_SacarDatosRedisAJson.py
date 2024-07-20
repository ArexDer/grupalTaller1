import json
import redis

# Configuración de conexión a Redis
redis_host = 'localhost'  # Cambia esto si Redis está en otro host
redis_port = 6379  # Puerto predeterminado de Redis
redis_db = 0  # Número de base de datos de Redis

# Nombre de la clave donde se guardaron los artículos en Redis
redis_key = 'articlesSISTEMAS'

# Nombre del archivo donde se guardarán los artículos recuperados
output_filename = "v4/articlesSistemas_recovered.json"

# Función para recuperar los artículos de Redis y guardarlos en un archivo JSON
def save_articles_from_redis(output_filename):
    try:
        # Conectar con Redis
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

        # Recuperar todos los artículos de Redis
        articles = r.lrange(redis_key, 0, -1)

        # Convertir los artículos a una lista de diccionarios
        articles_list = [json.loads(article) for article in articles]

        # Guardar los artículos en un archivo JSON
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(articles_list, outfile, ensure_ascii=False, indent=4)

        print(f"Los artículos se han guardado correctamente en {output_filename}.")

    except redis.ConnectionError:
        print(f"No se pudo conectar a Redis en {redis_host}:{redis_port}. Verifica la configuración de conexión.")
    except IOError as e:
        print(f"Error de escritura del archivo: {e}")

# Llamar a la función para guardar los artículos de Redis en un archivo JSON
save_articles_from_redis(output_filename)
