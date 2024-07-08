import random

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

            self.comprobar_informacion(ecosistema)

            if self.is_hambriento and self.alimentarse(ecosistema, reportes):
                return

            if self.is_sediento and self.beber(ecosistema, reportes):
                return

            if self.cansancio > 8:
                # Implementar lógica de descansar
                return

            if self.atacar(ecosistema, reportes):
                return

            if self.peso >= self.max_peso and self.aparearse(ecosistema, reportes):
                return

            if self.comunicar(ecosistema, reportes):
                return

            opcion = random.choice([True, False])

            if self.is_solo(ecosistema) and opcion and self.gritar(ecosistema, reportes):
                return

            if self.is_solo(ecosistema) and not opcion and self.acercarse(ecosistema, reportes):
                return

            if self.moverse(ecosistema, reportes):
                return

        hacer_accion()
        self.crecer(ecosistema, reportes)
