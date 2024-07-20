import re

# Suponiendo que 'filename' es el nombre del archivo donde guardaste los artículos
filename = "articlesSport.txt"

# Palabras específicas que queremos contar
words_to_count = ["Copa América", "Argentina", "Colombia", "Campeón", "Ganador", "2024", "Messi"]

try:
    # Abre el archivo en modo lectura ('r')
    with open(filename, 'r', encoding='utf-8') as file:
        articles = file.readlines()  # Lee todas las líneas del archivo

        word_count = {word: 0 for word in words_to_count}

        # Función para contar las palabras específicas
        def count_specific_words(text):
            for word in words_to_count:
                count = len(re.findall(r'\b' + re.escape(word) + r'\b', text, flags=re.IGNORECASE))
                word_count[word] += count

        # Procesar cada artículo
        for article in articles:
            count_specific_words(article)

        # Imprimir los resultados
        print("Cantidad de veces que aparecen las palabras específicas:")
        for word in words_to_count:
            print(f"{word}: {word_count[word]}")

except FileNotFoundError:
    print(f"El archivo '{filename}' no se encontró. Verifica el nombre del archivo o su ubicación.")
except IOError as e:
    print(f"Error de lectura del archivo: {e}")
