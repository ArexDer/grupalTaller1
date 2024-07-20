import json

filename_input = "v4/articlesSistemas.txt"  # Nombre de tu archivo de texto de entrada
filename_output = "v4/articlesSistemas_cleaned.txt"  # Nombre del archivo de salida para los artículos limpios

try:
    with open(filename_input, 'r', encoding='utf-8') as file_in, \
         open(filename_output, 'w', encoding='utf-8') as file_out:

        for line in file_in:
            try:
                # Convertir la línea a un diccionario Python
                article = eval(line.strip())

                # Eliminar los campos especificados
                fields_to_remove = ['uri', 'isDuplicate', 'date', 'time', 'dateTime', 'dateTimePub', 'sim','lang','dataType']
                for field in fields_to_remove:
                    if field in article:
                        del article[field]

                # Escribir el artículo limpio en el archivo de salida
                file_out.write(json.dumps(article, ensure_ascii=False) + '\n')

            except Exception as e:
                print(f"Error al procesar la línea: {e}")

    print(f"Los artículos limpios se han guardado en '{filename_output}'.")

except FileNotFoundError:
    print(f"El archivo '{filename_input}' no se encontró. Verifica el nombre del archivo o su ubicación.")
except IOError as e:
    print(f"Error de lectura/escritura del archivo: {e}")
