import json
from models.utils.Types_Enum import Tipo_Terreno


def load_json(nombre):
    ruta_archivo = f"data/{nombre}.json"

    try:
        with open(ruta_archivo, 'r') as archivo:
            datos = json.load(archivo)
        return datos
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_archivo}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: El archivo '{ruta_archivo}' no contiene un JSON válido")
        return None
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {str(e)}")
        return None


mapper_to_entity = {
    "S": Tipo_Terreno.SABANA,
    "D": Tipo_Terreno.DESIERTO,
    "P": Tipo_Terreno.PANTANO,
    "R": Tipo_Terreno.PRADERA,
    "A": Tipo_Terreno.ACANTILADO,
    "W": Tipo_Terreno.AGUA,
    "sabana": Tipo_Terreno.SABANA,
    "desierto": Tipo_Terreno.DESIERTO,
    "pradera": Tipo_Terreno.PRADERA,
    "pantano": Tipo_Terreno.PANTANO,
    "acantilado": Tipo_Terreno.ACANTILADO,
    "agua": Tipo_Terreno.AGUA,
}

mapper_to_name = {
    Tipo_Terreno.SABANA: "sabana",
    Tipo_Terreno.PANTANO: "pantano",
    Tipo_Terreno.PRADERA: "pradera",
    Tipo_Terreno.DESIERTO: "desierto",
    Tipo_Terreno.ACANTILADO: "acantilado",
    Tipo_Terreno.AGUA: "agua"
}


def cargar_mapa(id_map="1"):
    return load_json(f"mapa_{id_map}")


def personalidades_humano():
    return load_json("personalidades_humano"),
