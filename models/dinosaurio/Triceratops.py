import random

from models.animal.Herbivoro import Herbivoro
from models.utils.Types_Enum import Tipo_Terreno


class Triceratops(Herbivoro):
    def __init__(self, sexo="Macho", huevo=False):
        super().__init__(
            especie="Triceratops",
            convivencia="manada",
            peso=6,
            alcance_vision=5,
            alcance_accion=4,
            ataque=10,
            defensa=10,
            habitat=[Tipo_Terreno.DESIERTO, Tipo_Terreno.PRADERA],
            sexo=sexo,
            max_edad=25200,
            time_gestacion=180,
            edad_adulta=5760,
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

            if self.huir(ecosistema, reportes):
                return

            if not self.is_hambriento and self.aparearse(ecosistema, reportes):
                return

            if self.atacar(ecosistema, reportes):
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
