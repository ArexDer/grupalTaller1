from flask import Flask, jsonify, stream_with_context, Response, render_template, request
import json
import time
from collections import Counter

# Configuración
filename = "articlesSistemas_recovered.json"
block_size = 25
interval = 10 # segundos

# Crear la aplicación Flask
app = Flask(__name__)

# Contador global para acumular las frecuencias de las palabras
global_word_count = Counter()

# Contador para el número total de datos
total_data_count = 500  # Ajusta este valor según la cantidad total de datos

# Variable para verificar si los datos ya han sido procesados
data_processed = False

# Función para procesar los bloques de datos
def process_blocks():
    global data_processed
    if data_processed:
        return

    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        data_count = len(data)
        
        for i in range(0, len(data), block_size):
            block = data[i:i + block_size]
            word_count = Counter()
            
            for article in block:
                title = article.get('title', '')
                words = title.split()
                filtered_words = [word for word in words if len(word) >= 3]
                word_count.update(filtered_words)
            
            global_word_count.update(word_count)
            most_common_words = dict(global_word_count.most_common(20))
            yield most_common_words
            
            # Imprimir el progreso actual
            processed_data = i + block_size
            print(f"Procesados {processed_data} de {data_count} datos.")
            
            time.sleep(interval)
        
        # Cuando se procesen todos los datos, imprimir el mensaje
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
    final_word_count = dict(global_word_count.most_common(20))  # Cambiado a 20 para ajustar al gráfico
    return jsonify(final_word_count)

# Ruta para buscar palabras específicas
@app.route('/search')
def search():
    query = request.args.get('query', '')
    search_words = query.split()
    
    filtered_word_count = {word: count for word, count in global_word_count.items() if any(search_word in word for search_word in search_words)}
    
    return jsonify(filtered_word_count)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
