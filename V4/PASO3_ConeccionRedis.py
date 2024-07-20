import json
import redis

# Configuración de conexión a Redis
redis_host = 'localhost'  # Cambia esto si Redis está en otro host
redis_port = 6379  # Puerto predeterminado de Redis
redis_db = 0  # Número de base de datos de Redis

# Nombre de la clave donde se guardarán los artículos en Redis
redis_key = 'articlesSISTEMAS'

# Nombre del archivo con los artículos limpios
filename_cleaned = "v4/articlesSistemas_cleaned.txt"

# Función para cargar los artículos limpios en Redis
def load_articles_to_redis(filename):
    try:
        # Conectar con Redis
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

        # Abrir el archivo de artículos limpios
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    # Convertir la línea a un diccionario Python
                    article = json.loads(line.strip())

                    # Convertir el diccionario a JSON y subirlo a Redis
                    r.rpush(redis_key, json.dumps(article))

                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON: {e}")
                except Exception as e:
                    print(f"Error al procesar la línea: {e}")

        print("Los artículos se han cargado correctamente en Redis.")

    except redis.ConnectionError:
        print(f"No se pudo conectar a Redis en {redis_host}:{redis_port}. Verifica la configuración de conexión.")
    except IOError as e:
        print(f"Error de lectura del archivo: {e}")

# Llamar a la función para cargar los artículos a Redis
load_articles_to_redis(filename_cleaned)
