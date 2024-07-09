import random

from app.utils.info import objetos_en_area_accion
from models.utils.Types_Enum import Tipo_Entidad
from models.animal.Animal import Animal


class Herbivoro(Animal):
    def __init__(self, especie, *args, **kwargs):
        super().__init__(especie, Tipo_Entidad.HERBIVORO, *args, **kwargs)

    def alimentarse(self, ecosistema, reportes):
        objetos = objetos_en_area_accion(self, ecosistema)
        plantas = [obj for obj in objetos if obj.tipo == Tipo_Entidad.VEGETAL and obj.is_alive]
        if plantas:
            planta = random.choice(plantas)
            self.peso += planta.peso * 0.1
            planta.peso -= planta.peso * 0.1
            if planta.peso <= planta.min_peso:
                planta.is_alive = False
            reportes.append({
                "entidad": self,
                "tipo": "alimentarse",
                "detalles": {
                    "acción": "comer",
                    "objeto": planta.tipo,
                    "posicion": planta.posicion,
                    "resultado": "[0.1 T]"
                }
            })
