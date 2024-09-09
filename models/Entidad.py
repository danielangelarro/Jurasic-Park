from abc import ABC


class Entidad(ABC):
    def __init__(self, especie, peso, edad, habitat):
        self.especie = especie
        self.peso = peso
        self.edad = edad
        self.habitat = habitat

        self.posicion = (0, 0)
        self.is_alive = True