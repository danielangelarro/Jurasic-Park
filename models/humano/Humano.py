import random

from app.utils_map import load_json
from app.utils.info import is_sediento as info_is_sediento
from app.utils.info import is_hambriento as info_is_hambriento
from app.utils.info import is_solo as info_is_solo
from models.animal.Animal import Animal
from models.utils.Types_Enum import Tipo_Terreno
from models.utils.Types_Enum import Tipo_Entidad
from pydantic import BaseModel


class GeneticaHumana(BaseModel):
    Fuerza: int
    Velocidad: int
    Resistencia: int
    Inteligencia: int
    Adaptabilidad: int


class HabilidadHumana(BaseModel):
    Caza: int
    Pesca: int
    Recoleccion: int
    Exploracion: int


class Humano(Animal):
    def __init__(self, nombre, edad, personalidad, sexo="Macho", genetica=None, habilidades=None):
        super().__init__(
            especie="Humano",
            tipo=Tipo_Entidad.MIXTO,
            convivencia="manada",
            peso=4,
            sexo=sexo,
            alcance_vision=5,
            alcance_accion=1,
            ataque=0.5,
            defensa=0.5,
            habitat=[Tipo_Terreno.ALL],
            max_edad=36000,
            time_gestacion=270,
            edad_adulta=5400
        )

        self.nombre = nombre
        self.edad = edad * 360
        self.personalidad = personalidad
        self.sed = 0
        self.cansancio = 0
        self.posicion = (0, 0)

        data = load_json("personalidades_humano")[personalidad]
        self.genetica = genetica or GeneticaHumana(
            Fuerza=data["genetica"]["fuerza"],
            Velocidad=data["genetica"]["velocidad"],
            Resistencia=data["genetica"]["resistencia"],
            Inteligencia=data["genetica"]["inteligencia"],
            Adaptabilidad=data["genetica"]["adaptabilidad"]
        )
        self.habilidades = habilidades or HabilidadHumana(
            Caza=data["habilidades"]["caza"],
            Recoleccion=data["habilidades"]["recoleccion"],
            Pesca=data["habilidades"]["pesca"],
            Exploracion=data["habilidades"]["exploracion"]
        )

    def __str__(self):
        return (
            f"{super().__str__()} \n"
            f"Nombre: {self.nombre}\n"
            f"Personalidad: {self.personalidad}\n"
            f""
        )

    def __repr__(self):
        return self.__str__()

    @property
    def is_pregnant(self):
        return self.custodiando_huevo

    @is_pregnant.setter
    def is_pregnant(self, valor):
        self.custodiando_huevo = valor

    @property
    def is_hambriento(self):
        return info_is_hambriento(self)

    @property
    def is_sediento(self):
        return info_is_sediento(self)

    def modificar_estado(self, peso=0, sed=0, cansancio=0):
        peso = min(peso, self.max_peso / 4)
        self.peso = max(0, self.peso + peso)
        self.sed = max(0, self.sed + sed)
        self.cansancio = max(0, self.cansancio + cansancio)
