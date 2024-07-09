from models.animal.Animal import Animal
from models.utils.Types_Enum import Etapa_Edad
from queue import SimpleQueue


def is_hambriento(entidad_animal: Animal):
    alpha = (entidad_animal.min_peso + entidad_animal.max_peso) / 2
    return entidad_animal.peso <= alpha


def is_sediento(entidad_animal: Animal):
    return entidad_animal.sed > 3


def is_solo(entidad_animal: Animal, ecosistema):
    objetos = objetos_en_area_vision(entidad_animal, ecosistema)
    manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == entidad_animal.especie]

    return manada == []


def ataque(entidad_animal: Animal, ecosistema, presa):
    atk = entidad_animal._ataque * 2 if entidad_animal.custodiando_huevo else 1
    manada = [
        obj for obj in ecosistema.animales
        if obj.especie == entidad_animal.especie and
           presa in objetos_en_area_accion(obj, ecosistema)
    ]
    atk += sum([m._ataque * 0 if m.custodiando_huevo else 1 for m in manada])

    return atk


def defensa(entidad_animal: Animal, ecosistema):
    _defensa: float = entidad_animal._defensa
    objetos = entidad_animal.objetos_en_area_accion
    manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == entidad_animal.especie]
    _defensa += sum([m._ataque for m in manada])

    return _defensa


def get_etapa_edad(entidad_animal: Animal):
    if entidad_animal.edad <= 0:
        return Etapa_Edad.HUEVO
    if entidad_animal.edad < entidad_animal.edad_adulta:
        return Etapa_Edad.JOVEN
    return Etapa_Edad.ADULTO


def comprobar_informacion(entidad_animal: Animal, ecosistema):
    objetos_visibles = [
        obj for obj in entidad_animal.informacion_manada
        if posicion_en_area_vision(entidad_animal, ecosistema, obj.posicion)
    ]
    for obj in objetos_visibles:
        entidad_animal.informacion_manada.remove(obj)


def posicion_en_area_vision(entidad_animal: Animal, ecosistema, posicion):
    objetos = objetos_en_area_vision(entidad_animal, ecosistema)
    posiciones = [obj.posicion for obj in objetos]

    return posicion in posiciones


def posicion_en_area_accion(entidad_animal: Animal, ecosistema):
    objetos = []

    direcciones = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    visitados = set()

    queue = SimpleQueue()
    queue.put_nowait((entidad_animal.posicion, 0))
    visitados.add(entidad_animal.posicion)

    while not queue.empty():
        posicion, distancia = queue.get_nowait()

        for x, y in direcciones:
            nueva_posicion = (posicion[0] + x, posicion[1] + y)
            if (distancia <= entidad_animal.alcance_accion and nueva_posicion not in visitados and
                    ecosistema.es_posicion_valida(nueva_posicion, entidad_animal.habitat)):
                entidad = ecosistema.entidades_en_posicion(nueva_posicion)
                visitados.add(nueva_posicion)
                objetos.append(nueva_posicion)

                if not entidad or entidad_animal.especie == "pteranodonte":
                    queue.put_nowait((nueva_posicion, distancia + 1))

    return objetos


def objetos_en_area_accion(entidad_animal: Animal, ecosistema):
    posiciones = posicion_en_area_accion(entidad_animal, ecosistema)
    entidades = []

    for posicion in posiciones:
        entidades.extend(ecosistema.entidades_en_posicion(posicion))

    return entidades


def terreno_en_area_accion(entidad_animal: Animal, ecosistema):
    posiciones = posicion_en_area_accion(entidad_animal, ecosistema)
    terrenos = []

    for posicion in posiciones:
        terrenos.append({
            "tipo": ecosistema.terreno_en_posicion(posicion),
            "posicion": posicion
        })

    return terrenos


def objetos_en_area_vision(entidad_animal, ecosistema, aumento=1):
    objetos = []

    direcciones = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    visitados = set()

    queue = SimpleQueue()
    queue.put_nowait((entidad_animal.posicion, 0))
    visitados.add(entidad_animal.posicion)

    while not queue.empty():
        posicion, distancia = queue.get_nowait()

        for x, y in direcciones:
            nueva_posicion = (posicion[0] + x, posicion[1] + y)
            if (distancia <= entidad_animal.alcance_vision * aumento and
                    nueva_posicion not in visitados and ecosistema.es_posicion_valida(nueva_posicion)):
                visitados.add(nueva_posicion)
                queue.put_nowait((nueva_posicion, distancia + 1))
                objetos.extend(ecosistema.entidades_en_posicion(nueva_posicion))

    return objetos
