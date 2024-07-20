import json

def count_json_data(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            count = len(data)
            return count
    except FileNotFoundError:
        print(f"Error: El archivo '{json_file}' no se encontró.")
        return 0
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return 0
    except Exception as e:
        print(f"Error inesperado: {e}")
        return 0

# Nombre del archivo JSON a contar
json_file = 'v4/articlesSistemas_recovered.json'

# Llamada a la función para contar los datos
data_count = count_json_data(json_file)

# Mostrar el resultado
if data_count > 0:
    print(f"El archivo '{json_file}' contiene {data_count} datos.")
else:
    print("No se pudo contar los datos del archivo.")
