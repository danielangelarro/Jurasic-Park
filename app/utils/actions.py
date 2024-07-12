import math
import random

from app.utils.info import terreno_en_area_accion, objetos_en_area_accion, ataque, defensa, posicion_en_area_accion, \
    objetos_en_area_vision, is_hambriento, get_etapa_edad, is_solo
from models.animal.Animal import Animal
from models.utils.Types_Enum import Etapa_Edad, Tipo_Terreno, Tipo_Entidad


def crecer(entidad_animal, ecosistema, reportes):
    entidad_animal.peso -= 0.5

    if entidad_animal.is_alive:
        entidad_animal.edad += 1
        entidad_animal.sed += 1
        entidad_animal.sobrevivir += 1

        if entidad_animal.edad > entidad_animal.max_edad:
            entidad_animal.sed = 0
            entidad_animal.is_alive = False
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "muerte",
                "detalles": {
                    "causa": "edad"
                }
            })
            return False

        if get_etapa_edad(entidad_animal) == Etapa_Edad.ADULTO and entidad_animal.peso < entidad_animal.min_peso:
            entidad_animal.sed = 0
            entidad_animal.is_alive = False
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "muerte",
                "detalles": {
                    "causa": "hambre"
                }
            })
            return False

        if entidad_animal.sed > 7:
            entidad_animal.sed = 0
            entidad_animal.is_alive = False
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "muerte",
                "detalles": {
                    "causa": "sed"
                }
            })
            return False

    else:
        if get_etapa_edad(entidad_animal) != Etapa_Edad.HUEVO and entidad_animal.peso <= 0:
            entidad_animal.is_alive = False
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "muerte",
                "detalles": {
                    "causa": "descomposicion"
                }
            })

            if entidad_animal in ecosistema.animales:
                ecosistema.animales.remove(entidad_animal)
                ecosistema.cementerio_animales.append(entidad_animal)

            elif entidad_animal in ecosistema.humanos:
                ecosistema.humanos.remove(entidad_animal)
                ecosistema.cementerio_humanos.append(entidad_animal)

            return True
    return True


def beber(entidad_animal, ecosistema, reportes):
    terrenos = entidad_animal.terreno_en_area_accion

    for terreno in terrenos:
        if terreno[0] == Tipo_Terreno.AGUA:
            vecindades = ecosistema.posiciones_vecinas_libres(terreno[1])

            for vecindad in vecindades:
                if ecosistema.terreno_en_posicion(vecindad) != Tipo_Terreno.AGUA:
                    reportes.append({
                        "entidad": entidad_animal,
                        "tipo": "beber",
                        "detalles": {
                            "acción": "tomar_agua",
                            "resultado": f"en ({vecindad[0]},{vecindad[1]})"
                        }
                    })
                    entidad_animal.posicion = vecindad
                    entidad_animal.sed = 0
                    return True

    acercarse_terreno(entidad_animal, ecosistema, reportes, Tipo_Terreno.AGUA)
    return False


def atacar(entidad_animal, ecosistema, reportes):
    objetos = entidad_animal.objetos_en_area_accion
    presas = [
        obj for obj in objetos
        if obj.tipo == Tipo_Entidad.CARNIVORO and obj.especie != entidad_animal.especie
           and obj.is_alive and ataque(entidad_animal, ecosistema, obj) > defensa(obj, ecosistema)
    ]
    if presas:
        presa = random.choice(presas)
        presa.is_alive = False
        reportes.append({
            "entidad": entidad_animal,
            "tipo": "atacar",
            "detalles": {
                "acción": "atacar",
                "presa": {
                    "especie": presa.especie,
                    "posicion": presa.posicion
                },
                "resultado_ataque": f"{ataque(entidad_animal, ecosistema, presa)} vs {defensa(presa, ecosistema)}"
            }
        })
        return True
    return False


def moverse(entidad_animal, ecosistema, reportes):
    if entidad_animal.custodiando_huevo:
        entidad_animal.crias = [cria for cria in entidad_animal.crias if cria is not None]
        huevo = [cria for cria in entidad_animal.crias if get_etapa_edad(cria) == Etapa_Edad.HUEVO]
        if huevo:
            return

    posiciones = entidad_animal.posicion_en_area_accion

    if posiciones:
        nueva_posicion = random.choice(list(posiciones))
        reportes.append({
            "entidad": entidad_animal,
            "tipo": "moverse",
            "detalles": {
                "acción": "moverse",
                "resultado": f"a ({nueva_posicion[0]},{nueva_posicion[1]})"
            }
        })
        entidad_animal.posicion = nueva_posicion

        return True
    return False


def huir(entidad_animal, ecosistema, reportes):
    objetos = entidad_animal.objetos_en_area_vision
    posiciones = entidad_animal.posicion_en_area_accion
    predadores = [obj for obj in objetos if obj.tipo == Tipo_Entidad.CARNIVORO and obj.especie != entidad_animal.especie]

    direccion = (entidad_animal.posicion, 0)

    for posicion in posiciones:
        distance = 0
        for predador in predadores:
            distance += ecosistema.get_distance(posicion, predador.posicion)

        if direccion[1] < distance:
            direccion = (posicion, distance)

    if direccion[1] == 0:
        return False

    reportes.append({
        "entidad": entidad_animal,
        "tipo": "huir",
        "detalles": {
            "acción": "huir",
            "resultado": f"a ({direccion[0][0]},{direccion[0][1]})"
        }
    })
    entidad_animal.posicion = direccion[0]

    return True


def acercarse_terreno(entidad_animal, ecosistema, reportes, terrenos):
    objetos = entidad_animal.objetos_en_area_vision
    posiciones_vision = [obj.posicion for obj in objetos]

    posiciones = entidad_animal.posicion_en_area_accion
    posiciones = [pos for pos in posiciones_vision if ecosistema.terreno_en_posicion(pos) in [terrenos]]

    direccion = (entidad_animal.posicion, math.inf)

    for posicion in posiciones:
        distance = 0
        for pos_vision in posiciones_vision:
            distance += ecosistema.get_distance(posicion, pos_vision)

        if direccion[1] > distance:
            direccion = (posicion, distance)

    if direccion[1] == math.inf:
        return False

    reportes.append({
        "entidad": entidad_animal,
        "tipo": "acercarse",
        "detalles": {
            "acción": "acercarse",
            "terrenos": str(terrenos),
            "direccion": direccion,
            "resultado": f"a ({direccion[0][0]},{direccion[0][1]})"
        }
    })
    entidad_animal.posicion = direccion[0]

    return True


def acercarse(entidad_animal, ecosistema, reportes, aumento=2, especie=None):
    if not is_solo(entidad_animal, ecosistema):
        return False

    if especie is None:
        especie = entidad_animal.especie

    objetos = entidad_animal.objetos_en_area_vision
    posiciones = entidad_animal.posicion_en_area_accion
    manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == especie]

    direccion = (entidad_animal.posicion, math.inf)

    for posicion in posiciones:
        distance = 0
        for entidad in manada:
            distance += ecosistema.get_distance(posicion, entidad.posicion)

        if direccion[1] > distance:
            direccion = (posicion, distance)

    if direccion[1] == math.inf:
        return False

    reportes.append({
        "entidad": entidad_animal,
        "tipo": "acercarse",
        "detalles": {
            "acción": "acercarse",
            "especie": especie,
            "direccion": direccion,
            "resultado": f"a ({direccion[0][0]},{direccion[0][1]})"
        }
    })
    entidad_animal.posicion = direccion[0]

    return True


def gritar(entidad_animal, ecosistema, reportes):
    if not is_solo(entidad_animal, ecosistema):
        return False

    objetos = entidad_animal.objetos_en_area_vision
    manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == entidad_animal.especie]

    if manada:
        map(lambda x: x.informacion_manada.union(entidad_animal), manada)
        reportes.append({
            "entidad": entidad_animal,
            "tipo": "gritar",
            "detalles": {
                "acción": "gritar",
                "resultado": "perdido"
            }
        })
        return True
    return False


def comunicar(entidad_animal, ecosistema, reportes):
    objetos = entidad_animal.objetos_en_area_vision
    informacion = set()

    algo_que_comunicar = False
    for obj in objetos:
        if isinstance(obj, Animal):
            if entidad_animal.tipo == "herbivoro" and obj.tipo == Tipo_Entidad.CARNIVORO:
                informacion.add(obj)
                algo_que_comunicar = True
                reportes.append({
                    "entidad": entidad_animal,
                    "tipo": "comunicar",
                    "detalles": {
                        "acción": "ver",
                        "objeto": obj.especie,
                        "posicion": obj.posicion,
                        "resultado": "peligro"
                    }
                })
            elif entidad_animal.tipo == Tipo_Entidad.CARNIVORO and obj.tipo == "herbivoro":
                informacion.add(obj)
                algo_que_comunicar = True
                reportes.append({
                    "entidad": entidad_animal,
                    "tipo": "comunicar",
                    "detalles": {
                        "acción": "ver",
                        "objeto": obj.especie,
                        "posicion": obj.posicion,
                        "resultado": "comida"
                    }
                })

    if not algo_que_comunicar:
        return False

    manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == entidad_animal.especie]
    if manada:
        map(lambda x: x.informacion_manada.union(informacion), manada)
        return True
    return False


def aparearse(entidad_animal, ecosistema, reportes):
    if entidad_animal.sexo == "Macho" and entidad_animal.edad >= entidad_animal.edad_adulta:
        objetos = entidad_animal.objetos_en_area_accion
        animales = [obj for obj in objetos if isinstance(obj, Animal)]
        hembras = [
            obj for obj in animales
            if obj.especie == entidad_animal.especie
               and obj.sexo == "Hembra"
               and obj.edad >= entidad_animal.edad_adulta
               and not obj.custodiando_huevo
               and ecosistema.posiciones_vecinas_libres(obj.posicion)
        ]
        if hembras:
            hembra = hembras[0]
            posiciones_vecinas = ecosistema.posiciones_vecinas_libres(hembra.posicion)
            posicion_huevo = random.choice(posiciones_vecinas)
            nuevo_huevo = entidad_animal.__class__(sexo=random.choice(["Macho", "Hembra"]), huevo=True)
            nuevo_huevo.set_posicion(posicion_huevo[0], posicion_huevo[1])
            ecosistema.animales.append(nuevo_huevo)
            hembra.custodiando_huevo = True
            hembra.crias.append(nuevo_huevo)
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "aparearse",
                "detalles": {
                    "acción": "aparearse",
                    "resultado": f"[Huevo en ({posicion_huevo[0]},{posicion_huevo[1]})]"
                }
            })

            return True
    return False


# Acciones Humanas

def descansar(entidad_animal, ecosistema, reportes):
    entidad_animal.modificar_estado(cansancio=-50)
    reportes.append({
        "entidad": entidad_animal,
        "tipo": "descansar",
        "detalles": {
            "acción": "descansar",
            "resultado": f"Nivel de cansancio: {entidad_animal.cansancio}"
        }
    })
    return True


def cazar(entidad_animal, ecosistema, reportes):
    terrenos = entidad_animal.terreno_en_area_accion
    terrenos_caza = [
        obj for obj in terrenos
        if obj[0] in (Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA)
    ]

    if not terrenos_caza or entidad_animal.peso >= entidad_animal.max_peso or not is_hambriento(entidad_animal):
        acercarse_terreno(entidad_animal, ecosistema, reportes, [Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA])
        return False

    exito = (entidad_animal.genetica.Fuerza + entidad_animal.genetica.Velocidad + entidad_animal.genetica.Adaptabilidad) / 3
    comida_obtenida = max(0, int(exito * random.uniform(0.5, 1.5)))

    entidad_animal.inventario["comida"] += comida_obtenida
    entidad_animal.cansancio += 2
    entidad_animal.habilidades.Caza += 1 if exito > 50 else 0

    reportes.append({
        "entidad": entidad_animal,
        "tipo": "cazar",
        "detalles": {
            "acción": "cazar",
            "resultado": f"Comida obtenida: {comida_obtenida}. "
                         f"Nueva habilidad de caza: {entidad_animal.habilidades.Caza}. "
                         f"Nivel de cansancio: {entidad_animal.cansancio}"
        }
    })

    return True


def recolectar(entidad_animal, ecosistema, reportes):
    terrenos = entidad_animal.terreno_en_area_accion
    terrenos_recoleccion = [
        obj for obj in terrenos
        if obj[0] in (Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA)
    ]

    if not terrenos_recoleccion or entidad_animal.peso >= entidad_animal.max_peso or not is_hambriento(entidad_animal):
        acercarse_terreno(entidad_animal, ecosistema, reportes, [Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA])
        return False

    exito = (entidad_animal.genetica.Inteligencia + entidad_animal.genetica.Velocidad + entidad_animal.genetica.Adaptabilidad) / 3

    comida_obtenida = max(0, int(exito * random.uniform(0.5, 1.5)))
    entidad_animal.inventario["comida"] += comida_obtenida
    entidad_animal.cansancio += 1
    entidad_animal.habilidades.Recoleccion += 1 if exito > 50 else 0

    reportes.append({
        "entidad": entidad_animal,
        "tipo": "recolectar",
        "detalles": {
            "acción": "recolectar",
            "resultado": f"Recursos obtenidos: {comida_obtenida}. "
                         f"Nueva habilidad de recolección: {entidad_animal.habilidades.Recoleccion}. "
                         f"Nivel de cansancio: {entidad_animal.cansancio}"
        }
    })

    return True

def pescar(entidad_animal, ecosistema, reportes):
    terrenos = entidad_animal.terreno_en_area_accion
    terrenos_recoleccion = [
        obj for obj in terrenos
        if obj[0] == Tipo_Terreno.AGUA
    ]

    if not terrenos_recoleccion or entidad_animal.peso >= entidad_animal.max_peso or not is_hambriento(entidad_animal):
        acercarse_terreno(entidad_animal, ecosistema, reportes, [Tipo_Terreno.AGUA])
        return False

    exito = (entidad_animal.habilidades.Pesca + entidad_animal.genetica.Inteligencia + entidad_animal.genetica.Fuerza) / 3

    comida_obtenida = max(0, int(exito * random.uniform(0.5, 1.5)))
    entidad_animal.inventario["comida"] += comida_obtenida
    entidad_animal.cansancio += 1.5
    entidad_animal.habilidades.Pesca += 1 if exito > 50 else 0

    reportes.append({
        "entidad": entidad_animal,
        "tipo": "pescar",
        "detalles": {
            "acción": "pescar",
            "resultado": f"Peces obtenidos: {comida_obtenida}. "
                         f"Nueva habilidad de pesca: {entidad_animal.habilidades.Pesca}. "
                         f"Nivel de cansancio: {entidad_animal.cansancio}"
        }
    })

    return True


def alimentarse_humano(entidad_animal, ecosistema, reportes):
    if entidad_animal.is_hambriento and entidad_animal.inventario["comida"] > 0:

        hambre = entidad_animal.max_peso - entidad_animal.peso
        comida = min(hambre, entidad_animal.inventario["comida"])

        entidad_animal.inventario["comida"] -= comida
        entidad_animal.modificar_estado(peso=comida)

        reportes.append({
            "entidad": entidad_animal,
            "tipo": "alimentarse",
            "detalles": {
                "acción": "alimentarse",
                "comida": f"{comida}.",
                "peso": f"{entidad_animal.peso}"
            }
        })

        return True
    else:
        return False

def atacar_humano(entidad_animal, ecosistema, reportes):
    if atacar(entidad_animal, ecosistema, reportes):
        entidad_animal.modificar_estado(cansancio=15)
        return True
    return False


def moverse_humano(entidad_animal, ecosistema, reportes):
    if moverse(entidad_animal, ecosistema, reportes):
        distancia = entidad_animal.genetica.Velocidad * (1 + entidad_animal.genetica.Resistencia / 100)
        entidad_animal.modificar_estado(cansancio=int(distancia / 10))
        return True
    return False


def buscar_refugio(entidad_animal, ecosistema, reportes):
    # TODO: Implement this function
    return False


def construir(entidad_animal, ecosistema, reportes):
    # TODO: Implement this function
    return False


def aparearse_humano(entidad_animal, ecosistema, reportes):
    if entidad_animal.edad < entidad_animal.edad_adulta:
        return False

    if entidad_animal.sexo == "Hembra" and entidad_animal.is_pregnant:
        return False

    objetos = entidad_animal.objetos_en_area_accion
    humanos = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == 'Humano']
    posibles_parejas = [
        obj for obj in humanos
        if obj.especie == entidad_animal.especie
           and obj.sexo != entidad_animal.sexo
           and obj.edad >= entidad_animal.edad_adulta
           and not (obj.sexo == "Hembra" and obj.is_pregnant)
    ]

    if posibles_parejas:
        pareja = posibles_parejas[0]
        if entidad_animal.sexo == "Hembra":
            entidad_animal.is_pregnant = True
            entidad_animal.gestation_period = random.randint(240, 270)  # Periodo de gestación humano típico en días
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "aparearse",
                "detalles": {
                    "acción": "aparearse",
                    "resultado": f"[Embarazo iniciado]"
                }
            })
        else:
            pareja.is_pregnant = True
            pareja.gestation_period = random.randint(240, 270)
            reportes.append({
                "entidad": pareja,
                "tipo": "aparearse",
                "detalles": {
                    "acción": "aparearse",
                    "resultado": f"[Embarazo iniciado]"
                }
            })
        return True
    return False


def avanzar_gestacion(entidad_animal, ecosistema, reportes):
    if entidad_animal.sexo == "Hembra" and entidad_animal.is_pregnant:
        entidad_animal.gestation_period -= 1

        if entidad_animal.gestation_period <= 0:
            entidad_animal.is_pregnant = False
            nuevo_bebe = entidad_animal.__class__(
                nombre=f"{entidad_animal.nombre} Jr.",
                edad=0,
                genetica=entidad_animal.genetica, habilidades=entidad_animal.habilidades,
                personalidad=random.choice(["Cazador", "Recolector", "Explorador"]),
                sexo=random.choice(["Macho", "Hembra"])
            )
            entidad_animal.crias.append(nuevo_bebe)
            ecosistema.humanos.append(nuevo_bebe)
            reportes.append({
                "entidad": entidad_animal,
                "tipo": "crecer",
                "detalles": {
                    "acción": "dar a luz",
                    "resultado": f"Bebé ({nuevo_bebe.sexo}) nacido en "
                                 f"({entidad_animal.posicion[0]},{entidad_animal.posicion[1]})"
                }
            })


def crecer_humano(entidad_animal, ecosistema, reportes):
    avanzar_gestacion(entidad_animal, ecosistema, reportes)
    crecer(entidad_animal, ecosistema, reportes)
