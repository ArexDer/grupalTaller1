from flask import Flask, request, jsonify, stream_with_context, Response, render_template
import json
import redis
import time
from collections import Counter
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems

# Configura el cliente de Event Registry
er = EventRegistry(apiKey="7f3e1d23-cead-4c5b-8a7b-5e47da1e9586", allowUseOfArchive=False)

# Configuración
filename_input = "v4/articlesSistemas.txt"
filename_cleaned = "v4/articlesSistemas_cleaned.txt"
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
redis_key = 'articlesSISTEMAS'
output_filename = "v4/articlesSistemas_recovered.json"
block_size = 25
interval = 5  # segundos
total_data_count = 500  # Ajusta este valor según la cantidad total de datos

# Crear la aplicación Flask
app = Flask(__name__)

# Contador global para acumular las frecuencias de las palabras
global_word_count = Counter()
data_processed = False

# Función para procesar los bloques de datos
import itertools

def process_blocks():
    global data_processed
    if data_processed:
        return

    with open(filename_cleaned, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data_count = len(lines)
        
        for i in range(0, data_count, block_size):
            word_count = Counter()
            block = itertools.islice(lines, i, i + block_size)
            for line in block:
                try:
                    article = json.loads(line.strip())
                    title = article.get('title', '')
                    words = title.split()
                    filtered_words = [word for word in words if len(word) >= 3]
                    word_count.update(filtered_words)
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON: {e}")
                except Exception as e:
                    print(f"Error al procesar la línea: {e}")
            
            global_word_count.update(word_count)
            most_common_words = dict(global_word_count.most_common(20))
            yield most_common_words

            processed_data = i + block_size
            print(f"Procesados {processed_data} de {data_count} datos.")
            
            time.sleep(interval)
        
        print("DATOS COMPLETOS")
        data_processed = True

# Ruta para servir los datos procesados en streaming
@app.route('/stream')
def stream():
    def generate():
        for word_count in process_blocks():
            yield f"data:{json.dumps(word_count)}\n\n"
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

# Ruta para servir el archivo HTML
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para servir los resultados finales como JSON
@app.route('/results')
def results():
    if not data_processed:
        return jsonify({"error": "Los datos aún no se han procesado completamente."})
    final_word_count = dict(global_word_count.most_common(20))
    return jsonify(final_word_count)

# Ruta para manejar el formulario de búsqueda
@app.route('/search', methods=['POST'])
def search():
    concept1 = request.form.get('concept1')
    concept2 = request.form.get('concept2')

    microsoftUri = er.getConceptUri(concept1)
    googleUri = er.getConceptUri(concept2)

    q = QueryArticlesIter(
        conceptUri=QueryItems.OR([microsoftUri, googleUri])
    )

    with open(filename_input, 'w', encoding='utf-8') as file:
        for art in q.execQuery(er, sortBy="date", maxItems=500):
            file.write(str(art) + '\n')

    clean_articles()
    load_articles_to_redis(filename_cleaned)
    return jsonify({"message": "Artículos buscados y procesados correctamente."})

def clean_articles():
    try:
        with open(filename_input, 'r', encoding='utf-8') as file_in, \
             open(filename_cleaned, 'w', encoding='utf-8') as file_out:

            for line in file_in:
                try:
                    article = eval(line.strip())
                    fields_to_remove = ['uri', 'isDuplicate', 'date', 'time', 'dateTime', 'dateTimePub', 'sim','lang','dataType']
                    for field in fields_to_remove:
                        if field in article:
                            del article[field]
                    file_out.write(json.dumps(article, ensure_ascii=False) + '\n')
                except Exception as e:
                    print(f"Error al procesar la línea: {e}")

        print(f"Los artículos limpios se han guardado en '{filename_cleaned}'.")

    except FileNotFoundError:
        print(f"El archivo '{filename_input}' no se encontró.")
    except IOError as e:
        print(f"Error de lectura/escritura del archivo: {e}")

def load_articles_to_redis(filename):
    try:
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    article = json.loads(line.strip())
                    r.rpush(redis_key, json.dumps(article))
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON: {e}")
                except Exception as e:
                    print(f"Error al procesar la línea: {e}")
        print("Los artículos se han cargado correctamente en Redis.")
    except redis.ConnectionError:
        print(f"No se pudo conectar a Redis en {redis_host}:{redis_port}.")
    except IOError as e:
        print(f"Error de lectura del archivo: {e}")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
