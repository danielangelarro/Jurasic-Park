import random

from models.utils.Types_Enum import Tipo_Terreno
from app.utils import mapper_to_entity


class Ecosistema:
    def __init__(self, mapa):
        self.days = 0
        self.animales = []
        self.vegetacion = []
        self.datos_estadisticos = []
        self.dimensiones = (mapa["dimensiones"]["alto"], mapa["dimensiones"]["ancho"])
        self.terreno = [[None for _ in range(self.dimensiones[1])] for _ in range(self.dimensiones[0])]

        self.mapa = mapa
        self.load_map(mapa)

    def load_map(self, mapa):
        for i, row in enumerate(mapa["terrenos"]["mapa"]):
            for j, celd in enumerate(row):
                self.terreno[i][j] = mapper_to_entity[celd]

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
            x, y = random.choice(posiciones)
            animal.set_posicion(x, y)
            self.animales.append(animal)

    def agregar_vegetacion(self, planta):
        posiciones = self.get_posicion_vacia_en_terreno(planta.habitat)

        if posiciones:
            x, y = random.choice(posiciones)
            planta.set_posicion(x, y)
            self.vegetacion.append(planta)

    def entidades_en_posicion(self, posicion):
        entidades = [animal for animal in self.animales if animal.posicion == posicion]
        entidades.extend([planta for planta in self.vegetacion if planta.posicion == posicion])
        return entidades

    def terreno_en_posicion(self, posicion):
        return self.terreno[posicion[0]][posicion[1]]

    def get_posicion_vacia_en_terreno(self, terrenos):
        posiciones = []

        for x in range(self.dimensiones[0]):
            for y in range(self.dimensiones[1]):
                posicion = (x, y)
                if self.es_posicion_valida(posicion, terrenos) and not self.entidades_en_posicion(posicion):
                    posiciones.append(posicion)

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

    def ciclo(self):
        self.days += 1
        reportes = []
        for vegetal in self.vegetacion:
            vegetal.crecer(self, reportes)

        for animal in self.animales:
            animal.decidir_accion(self, reportes)
        return reportes

    def imprimir_estados(self):
        for animal in self.animales:
            print("\n", animal)