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

            if self.moverse(ecosistema, reportes):
                return

        hacer_accion()
        self.crecer(ecosistema, reportes)
