from app.utils.actions import beber, atacar, aparearse, moverse, crecer
from app.utils.info import comprobar_informacion, is_hambriento, is_sediento
from models.animal.Carnivoro import Carnivoro
from models.utils.Types_Enum import Tipo_Terreno


class Tiranosaurio(Carnivoro):
    def __init__(self, sexo="Macho", huevo=False):
        super().__init__(
            especie="Tiranosaurio",
            convivencia="solitario",
            peso=12,
            alcance_vision=6,
            alcance_accion=4,
            ataque=20,
            defensa=15,
            habitat=[Tipo_Terreno.DESIERTO, Tipo_Terreno.PRADERA],
            sexo=sexo,
            max_edad=10800,
            time_gestacion=0.6,
            edad_adulta=12,
            huevo=huevo
        )

    def decidir_accion(self, ecosistema, reportes):
        def hacer_accion(self=None):
            if not self.is_alive:
                return

            comprobar_informacion(self, ecosistema)

            if is_hambriento(self) and self.alimentarse(ecosistema, reportes):
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

            if moverse(self, ecosistema, reportes):
                return

        hacer_accion()
        crecer(self, ecosistema, reportes)
