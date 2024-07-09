import random

from app.utils.actions import atacar
from app.utils.info import objetos_en_area_accion, ataque, defensa, get_etapa_edad
from models.utils.Types_Enum import Tipo_Entidad, Etapa_Edad
from models.animal.Animal import Animal


class Carnivoro(Animal):
    def __init__(self, especie, *args, **kwargs):
        super().__init__(especie, Tipo_Entidad.CARNIVORO, *args, **kwargs)

    def atacar(self, ecosistema, reportes):
        if atacar(self, ecosistema, reportes):
            return

        objetos = objetos_en_area_accion(self, ecosistema)
        presas = [
            obj for obj in objetos
            if isinstance(obj, Animal) and obj.especie != self.especie and
               obj.is_alive and ataque(self, ecosistema, obj) > defensa(obj, ecosistema)
        ]
        if presas:
            presa = random.choice(presas)
            presa.is_alive = False
            reportes.append({
                "entidad": self,
                "tipo": "atacar",
                "detalles": {
                    "acción": "atacar",
                    "presa": {
                        "especie": presa.especie,
                        "posicion": presa.posicion
                    },
                    "resultado_ataque": f"{ataque(self, ecosistema, presa)} vs {defensa(presa, ecosistema)}"
                }
            })

    def alimentarse(self, ecosistema, reportes):
        objetos = objetos_en_area_accion(self, ecosistema)
        presas = [
            obj for obj in objetos
            if isinstance(obj, Animal) and
                (get_etapa_edad(obj) == Etapa_Edad.HUEVO or not obj.is_alive)
        ]
        if presas:
            presa = presas[0]
            self.peso += presa.peso * 0.5
            presa.peso -= presa.peso * 0.5
            reportes.append({
                "entidad": self,
                "tipo": "alimentarse",
                "detalles": {
                    "acción": "comer",
                    "objeto": presa.especie,
                    "posicion": presa.posicion,
                    "resultado": "[0.5 T]"
                }
            })
