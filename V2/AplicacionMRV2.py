import re
from collections import defaultdict

# Suponiendo que 'filename' es el nombre del archivo donde guardaste los artículos
filename = "articlesSport.txt"

# Palabras específicas que queremos contar
words_to_count = ["Copa América", "Argentina", "Colombia", "Campeón", "Ganador", "2024", "Messi"]

# Lista de palabras vacías en español e inglés
stop_words_es = [
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para",
    "con", "no", "una", "su", "al", "lo", "como", "más", "pero", "sus", "le", "ya", "o", "este",
    "sí", "porque", "esta", "entre", "cuando", "muy", "sin", "sobre", "también", "me", "hasta",
    "hay", "donde", "quien", "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra",
    "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué", "unos", "yo",
    "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho", "quienes", "nada", "muchos", "cual",
    "poco", "ella", "estar", "estas", "algunas", "algo", "nosotros", "mi", "mis", "tú", "te", "ti", "tu",
    "tus", "ellas", "nosotras", "vosotros", "vosotras", "os", "mío", "mía", "míos", "mías", "tuyo", "tuya",
    "tuyos", "tuyas", "suyo", "suya", "suyos", "suyas", "nuestro", "nuestra", "nuestros", "nuestras", "vuestro",
    "vuestra", "vuestros", "vuestras", "esos", "esas", "estoy", "estás", "está", "estamos", "estáis", "están",
    "esté", "estés", "estemos", "estéis", "estén", "estaré", "estarás", "estará", "estaremos", "estaréis", "estarán",
    "estaría", "estarías", "estaríamos", "estaríais", "estarían", "estaba", "estabas", "estábamos", "estabais", "estaban",
    "estuve", "estuviste", "estuvo", "estuvimos", "estuvisteis", "estuvieron", "estuviera", "estuvieras", "estuviéramos",
    "estuvierais", "estuvieran", "estuviese", "estuvieses", "estuviésemos", "estuvieseis", "estuviesen", "estando", "estado",
    "estada", "estados", "estadas", "estad", "he", "has", "ha", "hemos", "habéis", "han", "haya", "hayas", "hayamos", "hayáis",
    "hayan", "habré", "habrás", "habrá", "habremos", "habréis", "habrán", "habría", "habrías", "habríamos", "habríais", "habrían",
    "había", "habías", "habíamos", "habíais", "habían", "hube", "hubiste", "hubo", "hubimos", "hubisteis", "hubieron", "hubiera",
    "hubieras", "hubiéramos", "hubierais", "hubieran", "hubiese", "hubieses", "hubiésemos", "hubieseis", "hubiesen", "habiendo", "habido",
    "habida", "habidos", "habidas", "soy", "eres", "es", "somos", "sois", "son", "sea", "seas", "seamos", "seáis", "sean", "seré", "serás",
    "será", "seremos", "seréis", "serán", "sería", "serías", "seríamos", "seríais", "serían", "era", "eras", "éramos", "erais", "eran", "fui",
    "fuiste", "fue", "fuimos", "fuisteis", "fueron", "fuera", "fueras", "fuéramos", "fuerais", "fueran", "fuese", "fueses", "fuésemos", "fueseis",
    "fuesen", "sintiendo", "sentido", "sentida", "sentidos", "sentidas", "siente", "sentid", "tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen",
    "tenga", "tengas", "tengamos", "tengáis", "tengan", "tendré", "tendrás", "tendrá", "tendremos", "tendréis", "tendrán", "tendría", "tendrías",
    "tendríamos", "tendríais", "tendrían", "tenía", "tenías", "teníamos", "teníais", "tenían", "tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis",
    "tuvieron", "tuviera", "tuvieras", "tuviéramos", "tuvierais", "tuvieran", "tuviese", "tuvieses", "tuviésemos", "tuvieseis", "tuviesen", "teniendo",
    "tenido", "tenida", "tenidos", "tenidas", "tened"
]

stop_words_en = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
]

# Combinar listas de palabras vacías
stop_words = set(stop_words_es + stop_words_en)

try:
    # Abre el archivo en modo lectura ('r')
    with open(filename, 'r', encoding='utf-8') as file:
        articles = file.readlines()  # Lee todas las líneas del archivo

        word_count = defaultdict(int)

        # Definir expresión regular para encontrar palabras
        word_pattern = re.compile(r'\b\w+\b')

        # Función para limpiar y contar las palabras
        def count_words(text):
            matches = word_pattern.findall(text.lower())
            for match in matches:
                if match not in stop_words:
                    word_count[match] += 1

        # Procesar cada artículo
        for article in articles:
            count_words(article)

        # Imprimir los resultados
        print("Cantidad de veces que aparecen las palabras no conectores:")
        for word, count in sorted(word_count.items(), key=lambda item: item[1], reverse=True)[:10]:
            print(f"{word}: {count}")

except FileNotFoundError:
    print(f"El archivo '{filename}' no se encontró. Verifica el nombre del archivo o su ubicación.")
except IOError as e:
    print(f"Error de lectura del archivo: {e}")
