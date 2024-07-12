import random

import numpy as np
from colorama import init, Style
from app.utils.actions import *
from app.utils_map import load_json
from app.utils_map import mapper_to_entity
from app.utils_map import mapper_to_color
from models.humano.Humano import GeneticaHumana, HabilidadHumana, Humano
from models.utils.Types_Enum import Tipo_Terreno


class Ecosistema:
    def __init__(self, mapa):
        self.days = 0
        self.animales = []
        self.humanos = self.inicializar_poblacion_humana(10)
        self.cementerio_animales = []
        self.cementerio_humanos = []
        self.vegetacion = []
        self.datos_estadisticos = []
        self.dimensiones = (mapa["dimensiones"]["alto"], mapa["dimensiones"]["ancho"])
        self.terreno = [[None for _ in range(self.dimensiones[1])] for _ in range(self.dimensiones[0])]
        self.total_humanos = 0

        self.mapa = mapa
        self.load_map(mapa)
        self.decision_tree = load_json("decision_tree_humano")

    def load_map(self, mapa):
        for i, row in enumerate(mapa["terrenos"]["mapa"]):
            for j, celd in enumerate(row):
                self.terreno[i][j] = mapper_to_entity[celd]

    def reset(self):
        self.days = 0
        self.cementerio_animales = []
        self.cementerio_humanos = []
        self.datos_estadisticos = []

        self.humanos = [
            Humano(
                nombre=humano.nombre,
                edad=random.randint(20, 50),
                personalidad=humano.personalidad,
                genetica=humano.genetica,
                habilidades=humano.habilidades
            ) for humano in self.humanos
        ]


    def print_map(self):
        init()
        for i, row in enumerate(self.terreno):
            for j, celd in enumerate(row):
                entidad = self.entidades_en_posicion((i,j))
                entidad_repr = '  ' if not entidad else entidad[0].sexo
                match entidad_repr:
                    case "Hembra": entidad_repr = '👩‍🦰'
                    case "Macho": entidad_repr = '👨‍🦰'
                print(f"{mapper_to_color[celd]}{entidad_repr}", end="")
            print(Style.RESET_ALL)

    def get_distance(self, posicion1, posicion2):
        return abs(posicion1[0] - posicion2[0]) + abs(posicion1[1] - posicion2[1])

    def es_posicion_valida(self, posicion, habitat=[Tipo_Terreno.ALL]):
        x, y = posicion
        if 0 <= x < self.dimensiones[0] and 0 <= y < self.dimensiones[1]:
            if Tipo_Terreno.ALL in habitat or self.terreno[x][y] in habitat:
                return True
        return False

    def agregar_animal(self, animal):
        posiciones = self.get_posicion_vacia_en_terreno(animal.habitat)
        if posiciones:
            x, y = random.choice(list(posiciones))
            animal.set_posicion(x, y)
            self.animales.append(animal)

    def agregar_vegetacion(self, planta):
        posiciones = self.get_posicion_vacia_en_terreno(planta.habitat)
        if posiciones:
            x, y = random.choice(list(posiciones))
            planta.set_posicion(x, y)
            self.vegetacion.append(planta)

    def entidades_en_posicion(self, posicion):
        entidades = set([animal for animal in self.animales if animal.posicion == posicion])
        entidades.union([humano for humano in self.humanos if humano.posicion == posicion])
        entidades.union([planta for planta in self.vegetacion if planta.posicion == posicion])
        return entidades

    def terreno_en_posicion(self, posicion):
        return self.terreno[posicion[0]][posicion[1]]

    def get_posicion_vacia_en_terreno(self, terrenos):
        posiciones = set()

        for x in range(self.dimensiones[0]):
            for y in range(self.dimensiones[1]):
                posicion = (x, y)
                if self.es_posicion_valida(posicion, terrenos) and not self.entidades_en_posicion(posicion):
                    posiciones.add(posicion)

        return posiciones

    def posiciones_vecinas_libres(self, posicion):
        x, y = posicion
        posiciones = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
        return [pos for pos in posiciones if self.es_posicion_valida(pos)]

    def imprimir_estados(self):
        for animal in self.animales:
            print("\n", animal)

    def inicializar_poblacion_humana(self, tamano_poblacion):
        personalidades = ["Cazador", "Recolector", "Explorador"]
        return [
            Humano(
                nombre=f"Humano_{i}",
                edad=random.randint(20, 50),
                personalidad=random.choice(personalidades),
                # genetica=GeneticaHumana(
                #     Fuerza=random.randint(0, 100),
                #     Velocidad=random.randint(0, 100),
                #     Resistencia=random.randint(0, 100),
                #     Inteligencia=random.randint(0, 100),
                #     Adaptabilidad=random.randint(0, 100)
                # ),
                # habilidades=HabilidadHumana(
                #     Caza=random.randint(0, 100),
                #     Recoleccion=random.randint(0, 100),
                #     Pesca=random.randint(0, 100),
                #     Exploracion=random.randint(0, 100)
                # )
            ) for i in range(tamano_poblacion)
        ]

    def evaluar_aptitud(self, humano):
        return (humano.genetica.Fuerza + humano.genetica.Velocidad + humano.genetica.Resistencia +
                humano.genetica.Inteligencia + humano.genetica.Adaptabilidad +
                humano.habilidades.Caza + humano.habilidades.Recoleccion +
                humano.habilidades.Pesca + humano.habilidades.Exploracion)

    def seleccion(self):
        humanos = self.humanos + self.cementerio_humanos
        humanos = sorted(humanos, key=lambda h: h.sobrevivir, reverse=True)
        seleccionados = humanos[:len(humanos) // 2]

        return seleccionados

    def cruza(self, padre1, padre2):
        def promedio_genetica(padre1, padre2):
            return GeneticaHumana(
                Fuerza=(padre1.genetica.Fuerza + padre2.genetica.Fuerza) // 2,
                Velocidad=(padre1.genetica.Velocidad + padre2.genetica.Velocidad) // 2,
                Resistencia=(padre1.genetica.Resistencia + padre2.genetica.Resistencia) // 2,
                Inteligencia=(padre1.genetica.Inteligencia + padre2.genetica.Inteligencia) // 2,
                Adaptabilidad=(padre1.genetica.Adaptabilidad + padre2.genetica.Adaptabilidad) // 2
            )

        def promedio_habilidades(padre1, padre2):
            return HabilidadHumana(
                Caza=(padre1.habilidades.Caza + padre2.habilidades.Caza) // 2,
                Recoleccion=(padre1.habilidades.Recoleccion + padre2.habilidades.Recoleccion) // 2,
                Pesca=(padre1.habilidades.Pesca + padre2.habilidades.Pesca) // 2,
                Exploracion=(padre1.habilidades.Exploracion + padre2.habilidades.Exploracion) // 2
            )

        hijo1 = Humano(
            nombre=f"Hijo1_{padre1.nombre}_{padre2.nombre}",
            edad=0,
            personalidad=random.choice([padre1.personalidad, padre2.personalidad]),
            genetica=promedio_genetica(padre1, padre2),
            habilidades=promedio_habilidades(padre1, padre2)
        )
        hijo2 = Humano(
            nombre=f"Hijo2_{padre1.nombre}_{padre2.nombre}",
            edad=0,
            personalidad=random.choice([padre1.personalidad, padre2.personalidad]),
            genetica=promedio_genetica(padre1, padre2),
            habilidades=promedio_habilidades(padre1, padre2)
        )

        return hijo1, hijo2

    def mutacion(self, humano):
        atributo_a_mutar = random.choice(['Fuerza', 'Velocidad', 'Resistencia', 'Inteligencia', 'Adaptabilidad',
                                          'Caza', 'Recoleccion', 'Pesca', 'Exploracion'])
        valor = random.randint(0, 100)
        setattr(humano.genetica, atributo_a_mutar, valor) if atributo_a_mutar in ['Fuerza', 'Velocidad', 'Resistencia',
                                                                                   'Inteligencia', 'Adaptabilidad'] else setattr(
            humano.habilidades, atributo_a_mutar, valor)

        return humano

    def evolucionar(self, generaciones=100):
        # for generacion in range(generaciones):

        seleccionados = self.seleccion()
        nuevos_humanos = []
        for i in range(0, len(seleccionados), 2):
            if i + 1 < len(seleccionados):
                hijo1, hijo2 = self.cruza(seleccionados[i], seleccionados[i + 1])
                self.mutacion(hijo1)
                self.mutacion(hijo2)
                nuevos_humanos.append(hijo1)
                nuevos_humanos.append(hijo2)
        self.humanos = seleccionados + nuevos_humanos

    def ciclo(self):
        self.days += 1
        reportes = []

        for vegetal in self.vegetacion:
            vegetal.crecer()

        for animal in self.animales + self.humanos:
            animal.objetos_en_area_vision = objetos_en_area_vision(animal, self)
            animal.objetos_en_area_accion = objetos_en_area_accion(animal, self)
            animal.posicion_en_area_accion = posicion_en_area_accion(animal, self)
            animal.terreno_en_area_accion = terreno_en_area_accion(animal, self)

            animal.decidir_accion(self, reportes)

        for animal in self.animales:
            if not animal.is_alive:
                self.animales.remove(animal)
                self.cementerio_animales.append(animal)

        for humano in self.humanos:
            if not humano.is_alive:
                self.humanos.remove(humano)
                self.cementerio_humanos.append(humano)

        return reportes

    def run(self, dias=30):
        for _ in range(dias):
            self.ciclo()
