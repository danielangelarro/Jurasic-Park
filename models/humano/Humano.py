import random

from pydantic import BaseModel
from scipy.stats import norm

from app.utils.actions import cazar, recolectar, pescar, descansar, construir, buscar_refugio, huir, atacar_humano, \
    beber, moverse_humano, gritar, acercarse, aparearse_humano, comunicar, crecer_humano, alimentarse_humano
from app.utils_map import load_json
from app.utils.info import is_sediento as info_is_sediento, get_etapa_edad
from app.utils.info import is_hambriento as info_is_hambriento
from models.animal.Animal import Animal
from models.utils.Types_Enum import Tipo_Terreno, Etapa_Edad
from models.utils.Types_Enum import Tipo_Entidad


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
            alcance_accion=2,
            ataque=0.5,
            defensa=0.5,
            habitat=[Tipo_Terreno.SABANA],
            max_edad=36000,
            time_gestacion=270,
            edad_adulta=5400,
        )

        self.nombre = nombre
        self.edad = edad * 360
        self.personalidad = personalidad
        self.sed = 0
        self.cansancio = 0
        self.posicion = (0, 0)
        self.inventario = {"comida": 0}

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

        self.acciones = ["cazar", "recolectar", "pescar", "descansar", "construir", "buscar_refugio",
            "huir", "comunicar", "aparearse", "acercarse", "gritar", "moverse", "beber", "atacar", "alimentarse"]

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

    def decidir_accion(self, ecosistema, reportes):

        crecer_humano(self, ecosistema, reportes)

        if not self.is_alive:
            return

        # Asignar probabilidades a las acciones basadas en genética y habilidades
        def get_probabilidad(accion):
            if accion == "cazar":
                return norm(loc=self.habilidades.Caza / 100, scale=0.1).rvs()
            elif accion == "recolectar":
                return norm(loc=self.habilidades.Recoleccion / 100, scale=0.1).rvs()
            elif accion == "pescar":
                return norm(loc=self.habilidades.Pesca / 100, scale=0.1).rvs()
            elif accion == "explorar":
                return norm(loc=self.habilidades.Exploracion / 100, scale=0.1).rvs()
            elif accion == "descansar":
                return norm(loc=0.9, scale=0.1).rvs()
            elif accion == "construir":
                return norm(loc=0.2, scale=0.1).rvs()
            elif accion == "buscar_refugio":
                return norm(loc=0.8, scale=0.1).rvs()
            elif accion == "huir":
                return norm(loc=0.7, scale=0.1).rvs()
            elif accion == "comunicar":
                return norm(loc=0.3, scale=0.1).rvs()
            elif accion == "aparearse":
                return norm(loc=0.5, scale=0.1).rvs()
            elif accion == "acercarse":
                return norm(loc=0.4, scale=0.1).rvs()
            elif accion == "gritar":
                return norm(loc=0.1, scale=0.05).rvs()
            elif accion == "moverse":
                return norm(loc=0.6, scale=0.1).rvs()
            elif accion == "beber":
                return norm(loc=0.95, scale=0.1).rvs()
            elif accion == "alimentarse":
                return norm(loc=0.90, scale=0.1).rvs()
            elif accion == "atacar":
                return norm(loc=0.4, scale=0.1).rvs()

        # Evaluar las acciones posibles y sus probabilidades
        acciones_probabilidades = {accion: get_probabilidad(accion) for accion in self.acciones}

        # Filtrar acciones posibles basadas en objetos y terreno visibles/accesibles
        acciones_posibles = {accion: prob for accion, prob in acciones_probabilidades.items() if
                             self.es_accion_posible(accion, self.objetos_en_area_vision, self.objetos_en_area_accion)}

        # Seleccionar acciones cuya suma de probabilidades sea menor o igual a 1
        acciones_seleccionadas = []
        suma_probabilidades = 0

        if "beber" in acciones_posibles:
            acciones_seleccionadas.append("beber")
            acciones_posibles.pop("beber")

        if "alimentarse" in acciones_posibles:
            acciones_seleccionadas.append("alimentarse")
            acciones_posibles.pop("alimentarse")

        acciones_posibles = [a for a, _ in acciones_posibles.items()]
        random.shuffle(acciones_posibles)
        acciones_seleccionadas += acciones_posibles[:4 - len(acciones_seleccionadas)]

        # for accion, prob in sorted(acciones_posibles.items(), key=lambda x: x[1], reverse=True)[:3]:
        #     if suma_probabilidades + prob <= 1:
        #         acciones_seleccionadas.append(accion)
        #         suma_probabilidades += prob

        # Ejecutar las acciones seleccionadas
        for accion in acciones_seleccionadas:
            self.ejecutar_accion(accion, ecosistema, reportes)

    def es_accion_posible(self, accion, objetos_visibles, objetos_accesibles):
        probabilidad = 0

        if accion == "cazar" and self.habilidades.Caza > 70:
            probabilidad = (self.genetica.Fuerza + self.genetica.Velocidad + self.genetica.Adaptabilidad
                            + self.habilidades.Caza) / 40
        elif accion == "recolectar"  and self.habilidades.Recoleccion > 60:
            probabilidad = (self.genetica.Inteligencia + self.genetica.Velocidad + self.genetica.Adaptabilidad
                            + self.habilidades.Recoleccion) / 40
        elif (accion == "pescar"  and self.habilidades.Pesca > 50
              and any(obj.tipo == Tipo_Terreno.AGUA for obj in objetos_accesibles)):
            probabilidad = (self.habilidades.Pesca + self.genetica.Inteligencia + self.genetica.Fuerza) / 40
        elif accion == "beber" and self.is_sediento:
            probabilidad = 1.0
        elif accion == "alimentarse" and self.is_hambriento:
            probabilidad = 1.0
        elif accion == "descansar" and self.cansancio > 70:
            probabilidad = 1.0
        elif accion == "buscar_refugio" and self.genetica.Adaptabilidad < 50:
            return False
        elif accion == "huir" and self.genetica.Velocidad > 60:
            probabilidad = (self.genetica.Velocidad + self.genetica.Resistencia + self.genetica.Adaptabilidad) / 40
        elif accion == "comunicar" and self.genetica.Inteligencia > 50:
            probabilidad = (self.genetica.Inteligencia + self.genetica.Adaptabilidad) / 20
        elif accion == "aparearse" and any(
                obj.especie == "Humano" for obj in objetos_accesibles
                if isinstance(obj, Animal) and obj.sexo != self.sexo and not self.is_pregnant and not obj.is_pregnant
                and get_etapa_edad(self) == Etapa_Edad.ADULTO and get_etapa_edad(obj) == Etapa_Edad.ADULTO):
            probabilidad = 1.0
        elif accion == "moverse":
            probabilidad = (self.genetica.Velocidad + self.genetica.Resistencia + self.genetica.Adaptabilidad) / 30

        return random.random() < probabilidad

    def ejecutar_accion(self, accion, ecosistema, reportes):
        # Lógica para ejecutar la acción seleccionada
        if accion == "cazar":
            cazar(self, ecosistema, reportes)
        elif accion == "recolectar":
            recolectar(self, ecosistema, reportes)
        elif accion == "pescar":
            pescar(self, ecosistema, reportes)
        elif accion == "descansar":
            descansar(self, ecosistema, reportes)
        elif accion == "construir":
            construir(self, ecosistema, reportes)
        elif accion == "buscar_refugio":
            buscar_refugio(self, ecosistema, reportes)
        elif accion == "huir":
            huir(self, ecosistema, reportes)
        elif accion == "comunicar":
            comunicar(self, ecosistema, reportes)
        elif accion == "aparearse":
            aparearse_humano(self, ecosistema, reportes)
        elif accion == "acercarse":
            acercarse(self, ecosistema, reportes)
        elif accion == "gritar":
            gritar(self, ecosistema, reportes)
        elif accion == "moverse":
            moverse_humano(self, ecosistema, reportes)
        elif accion == "beber":
            beber(self, ecosistema, reportes)
        elif accion == "alimentarse":
            alimentarse_humano(self, ecosistema, reportes)
        elif accion == "atacar":
            atacar_humano(self, ecosistema, reportes)
