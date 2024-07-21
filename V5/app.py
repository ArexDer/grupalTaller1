from flask import Flask, render_template, request, jsonify
import json
import redis
import time
import os
from collections import Counter
from threading import Thread
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems

app = Flask(__name__)

# Configura el cliente de Event Registry
er = EventRegistry(apiKey="7f3e1d23-cead-4c5b-8a7b-5e47da1e9586", allowUseOfArchive=False)

# Configuración de conexión a Redis
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

redis_key = 'articlesSISTEMAS'
batch_size = 25
interval = 5
max_articles = 1500  # Este valor se puede ajustar según sea necesario

# Archivo para almacenar el conteo global de palabras
global_word_count_file = "global_word_count.json"

def initialize_global_word_count():
    if not os.path.exists(global_word_count_file):
        with open(global_word_count_file, 'w', encoding='utf-8') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)

def reset_global_word_count():
    with open(global_word_count_file, 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)

initialize_global_word_count()

def process_word_count(word_count):
    return {word: count for word, count in word_count.items() if len(word) >= 3}

def update_global_word_count(word_count):
    try:
        with open(global_word_count_file, 'r+', encoding='utf-8') as file:
            global_word_count = json.load(file)
            global_word_count_counter = Counter(global_word_count)
            global_word_count_counter.update(word_count)
            global_word_count = dict(global_word_count_counter)
            file.seek(0)
            json.dump(global_word_count, file, ensure_ascii=False, indent=4)
    except IOError:
        pass

def background_task():
    r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
    total_articles_processed = 0
    total_articles_in_redis = r.llen(redis_key)

    while total_articles_processed < total_articles_in_redis:
        articles = []
        for _ in range(batch_size):
            article = r.lpop(redis_key)
            if article:
                articles.append(json.loads(article))
            else:
                break
        if articles:
            word_count = Counter()
            for article in articles:
                word_count.update(article.get("title", "").split())

            word_count = process_word_count(word_count)
            update_global_word_count(word_count)
            
            total_articles_processed += len(articles)
            time.sleep(interval)
        else:
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    term1 = request.form.get('term1')
    term2 = request.form.get('term2')

    term1Uri = er.getConceptUri(term1)
    term2Uri = er.getConceptUri(term2)

    q = QueryArticlesIter(
        conceptUri=QueryItems.OR([term1Uri, term2Uri]),
    )

    articles = []
    for art in q.execQuery(er, sortBy="date", maxItems=max_articles):
        articles.append({
            "title": art.get("title"),
            "body": art.get("body"),
            "date": art.get("date"),
            "url": art.get("url")
        })

    filename = "articlesSistemas.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(articles, file, ensure_ascii=False, indent=4)

    articles_found = len(articles)
    articles_needed = max_articles
    message = f"Se encontraron {articles_found} de los {articles_needed} artículos solicitados."

    # Reiniciar el conteo global de palabras antes de cargar nuevos datos
    reset_global_word_count()

    return render_template('index.html', message=message, articles_found=articles_found, articles_needed=articles_needed)

@app.route('/load_to_redis', methods=['POST'])
def load_to_redis():
    try:
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

        with open("articlesSistemas.json", 'r', encoding='utf-8') as file:
            articles = json.load(file)
            for article in articles:
                r.rpush(redis_key, json.dumps(article))

        message = "Los artículos se han cargado correctamente en Redis."
    except redis.ConnectionError:
        message = f"No se pudo conectar a Redis en {redis_host}:{redis_port}. Verifica la configuración de conexión."
    except IOError as e:
        message = f"Error de lectura del archivo: {e}"
    except Exception as e:
        message = f"Error al cargar los artículos a Redis: {e}"

    return render_template('index.html', message=message)

@app.route('/start_processing', methods=['POST'])
def start_processing():
    # Inicia el procesamiento en segundo plano
    Thread(target=background_task, daemon=True).start()
    return jsonify({"status": "Processing started"})

@app.route('/get_global_word_count', methods=['GET'])
def get_global_word_count():
    try:
        with open(global_word_count_file, 'r', encoding='utf-8') as file:
            word_count = json.load(file)
        word_count = process_word_count(word_count)
        return jsonify(word_count)
    except IOError:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
