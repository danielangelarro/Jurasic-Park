import random

from app.utils.actions import beber, atacar, aparearse, comunicar, gritar, acercarse, moverse, crecer
from app.utils.info import comprobar_informacion, is_hambriento, is_sediento, is_solo
from models.animal.Herbivoro import Herbivoro
from models.utils.Types_Enum import Tipo_Terreno


class Braquiosaurio(Herbivoro):
    def __init__(self, sexo="Macho", huevo=False):
        super().__init__(
            especie="Braquiosaurio",
            convivencia="manada",
            peso=15,
            alcance_vision=5,
            alcance_accion=3,
            ataque=5,
            defensa=10,
            habitat=[Tipo_Terreno.PANTANO, Tipo_Terreno.DESIERTO, Tipo_Terreno.PRADERA],
            sexo=sexo,
            max_edad=36000,
            time_gestacion=180,
            edad_adulta=7200,
            huevo=huevo
        )

    def decidir_accion(self, ecosistema, reportes):

        def hacer_accion():
            if not self.is_alive:
                return

            comprobar_informacion(self, ecosistema)

            if is_hambriento(self) and super().alimentarse(ecosistema, reportes):
                return

            if is_sediento(self) and beber(self, ecosistema, reportes):
                return

            if self.cansancio > 8:
                # Implementar lógica de descansar
                return

            if atacar(self, ecosistema, reportes):
                return

            if self.peso >= self.max_peso and aparearse(self, ecosistema, reportes):
                return

            if comunicar(self, ecosistema, reportes):
                return

            opcion = random.choice([True, False])

            if is_solo(self, ecosistema) and opcion and gritar(self, ecosistema, reportes):
                return

            if is_solo(self, ecosistema) and not opcion and acercarse(self, ecosistema, reportes):
                return

            if moverse(self, ecosistema, reportes):
                return

        hacer_accion()
        crecer(self, ecosistema, reportes)
