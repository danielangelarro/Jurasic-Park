import random

from app.utils import load_json
from app.utils import mapper_to_name
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

    def modificar_estado(self, peso=0, sed=0, cansancio=0):
        peso = min(peso, self.max_peso / 4)
        self.peso = max(0, self.peso + peso)
        self.sed = max(0, self.sed + sed)
        self.cansancio = max(0, self.cansancio + cansancio)

    def descansar(self, ecosistema, reportes):
        self.modificar_estado(cansancio=-50)
        reportes.append({
            "entidad": self,
            "tipo": "descansar",
            "detalles": {
                "acción": "descansar",
                "resultado": f"Nivel de cansancio: {self.cansancio}"
            }
        })
        return True

    def cazar(self, ecosistema, reportes):
        terrenos = super().terreno_en_area_accion(ecosistema)
        terrenos_caza = [
            obj for obj in terrenos
            if obj["tipo"] in (Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA)
        ]

        if not terrenos_caza or self.peso >= self.max_peso or not self.is_hambriento:
            self.acercarse_terreno(ecosistema, reportes, [Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA])
            return False

        exito = (self.genetica.Fuerza + self.genetica.Velocidad + self.genetica.Adaptabilidad) / 3
        self.habilidades.Caza += 1 if exito > 50 else 0
        comida_obtenida = exito / 10
        self.modificar_estado(peso=int(comida_obtenida), cansancio=10)
        reportes.append({
            "entidad": self,
            "tipo": "cazar",
            "detalles": {
                "acción": "cazar",
                "resultado": f"Comida obtenida: {comida_obtenida}. "
                             f"Nueva habilidad de caza: {self.habilidades.Caza}. "
                             f"Nivel de peso: {self.peso}. "
                             f"Nivel de cansancio: {self.cansancio}"
            }
        })

        return True

    def recolectar(self, ecosistema, reportes):
        terrenos = super().terreno_en_area_accion(ecosistema)
        terrenos_recoleccion = [
            obj for obj in terrenos
            if obj["tipo"] in (Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA)
        ]

        if not terrenos_recoleccion or self.peso >= self.max_peso or not self.is_hambriento:
            self.acercarse_terreno(ecosistema, reportes, [Tipo_Terreno.SABANA, Tipo_Terreno.PRADERA])
            return False

        exito = (self.genetica.Inteligencia + self.genetica.Velocidad + self.genetica.Adaptabilidad) / 3
        self.habilidades.Recoleccion += 1 if exito > 50 else 0
        recursos_obtenidos = exito / 10
        self.modificar_estado(peso=int(recursos_obtenidos), cansancio=5)
        reportes.append({
            "entidad": self,
            "tipo": "recolectar",
            "detalles": {
                "acción": "recolectar",
                "resultado": f"Recursos obtenidos: {recursos_obtenidos}. "
                             f"Nueva habilidad de recolección: {self.habilidades.Recoleccion}. "
                             f"Nivel de peso: {self.peso}. "
                             f"Nivel de cansancio: {self.cansancio}"
            }
        })

        return True

    def pescar(self, ecosistema, reportes):
        terrenos = super().terreno_en_area_accion(ecosistema)
        terrenos_recoleccion = [
            obj for obj in terrenos
            if obj["tipo"] == Tipo_Terreno.AGUA
        ]

        if not terrenos_recoleccion or self.peso >= self.max_peso or not self.is_hambriento:
            self.acercarse_terreno(ecosistema, reportes, [Tipo_Terreno.AGUA])
            return False

        exito = (self.habilidades.Pesca + self.genetica.Inteligencia + self.genetica.Fuerza) / 3
        self.habilidades.Pesca += 1 if exito > 50 else 0
        peces_obtenidos = exito / 10
        self.modificar_estado(peso=int(peces_obtenidos), cansancio=5)
        reportes.append({
            "entidad": self,
            "tipo": "pescar",
            "detalles": {
                "acción": "pescar",
                "resultado": f"Peces obtenidos: {peces_obtenidos}. "
                             f"Nueva habilidad de pesca: {self.habilidades.Pesca}. "
                             f"Nivel de peso: {self.peso}. "
                             f"Nivel de cansancio: {self.cansancio}"
            }
        })

        return True

    def atacar(self, ecosistema, reportes):
        if super().atacar(ecosistema, reportes):
            self.modificar_estado(cansancio=15)
            return True
        return False

    def moverse(self, ecosistema, reportes):
        if super().moverse(ecosistema, reportes):
            distancia = self.genetica.Velocidad * (1 + self.genetica.Resistencia / 100)
            self.modificar_estado(cansancio=int(distancia / 10))
            return True
        return False

    def buscar_refugio(self, ecosistema, reportes):
        # TODO: Implement this function
        return False

    def construir(self, ecosistema, reportes):
        # TODO: Implement this function
        return False

    def aparearse(self, ecosistema, reportes):
        if self.edad < self.edad_adulta:
            return False

        if self.sexo == "Hembra" and self.is_pregnant:
            return False

        objetos = self.objetos_en_area_accion(ecosistema)
        humanos = [obj for obj in objetos if isinstance(obj, Humano)]
        posibles_parejas = [
            obj for obj in humanos
            if obj.especie == self.especie
               and obj.sexo != self.sexo
               and obj.edad >= self.edad_adulta
               and not (obj.sexo == "Hembra" and obj.is_pregnant)
               # and ecosistema.posiciones_vecinas_libres(obj.posicion)
        ]

        if posibles_parejas:
            pareja = posibles_parejas[0]
            if self.sexo == "Hembra":
                self.is_pregnant = True
                self.gestation_period = random.randint(240, 270)  # Periodo de gestación humano típico en días
                reportes.append({
                    "entidad": self,
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

    def avanzar_gestacion(self, ecosistema, reportes):
        if self.sexo == "Hembra" and self.is_pregnant:
            self.gestation_period -= 1
            if self.gestation_period <= 0:
                self.is_pregnant = False
                nuevo_bebe = Humano(
                    nombre=f"{self.nombre} Jr.",
                    edad=0,
                    genetica=self.genetica, habilidades=self.habilidades,
                    personalidad=random.choice(["Cazador", "Recolector", "Explorador"]),
                    sexo=random.choice(["Macho", "Hembra"])
                )
                self.crias.append(nuevo_bebe)
                ecosistema.animales.append(nuevo_bebe)
                reportes.append({
                    "entidad": self,
                    "tipo": "crecer",
                    "detalles": {
                        "acción": "dar a luz",
                        "resultado": f"Bebé ({nuevo_bebe.sexo}) nacido en ({self.posicion[0]},{self.posicion[1]})"
                    }
                })

    def crecer(self, ecosistema, reportes):
        self.avanzar_gestacion(ecosistema, reportes)
        super().crecer(ecosistema, reportes)

    def get_all_attributes(self):
        attributes = {}
        for cls in self.__class__.__mro__:
            for key, value in cls.__dict__.items():
                if isinstance(value, property):
                    attributes[key] = getattr(self, key)
                elif not key.startswith('__') and not key.endswith('__'):
                    attributes[key] = value
        attributes.update(self.__dict__)
        return attributes

    def decidir_accion(self, ecosistema, reportes):
        decision_tree = load_json("decision_tree")
        terrenos = [terreno["tipo"] for terreno in self.terreno_en_area_accion(ecosistema)]
        terrenos = set([mapper_to_name[terreno] for terreno in terrenos])

        def hacer_accion():
            if not self.is_alive:
                return False

            for accion in acciones:
                condition = accion["condition"]
                if eval(condition, {}, self.get_all_attributes()):
                    metodo = accion["true"]
                    if metodo == "return":
                        return False
                    if hasattr(self, metodo):
                        if getattr(self, metodo)(ecosistema, reportes):
                            return True
            return False

        accion_realizada = False
        for terreno in terrenos:
            acciones = decision_tree[terreno]["acciones"]
            if hacer_accion():
                accion_realizada = True
                break

        if not accion_realizada:
            self.moverse(ecosistema, reportes)
        self.crecer(ecosistema, reportes)
