from models.vegetacion.Frutales import Frutal
from models.utils.Types_Enum import Tipo_Terreno


class Baya(Frutal):
    def __init__(self):
        super().__init__(
            especie="Baya",
            peso=1,
            max_peso=3,
            edad=7,
            edad_adulta=3,
            alcance=5,
            habitat=[Tipo_Terreno.SABANA]
        )
