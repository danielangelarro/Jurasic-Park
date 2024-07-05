from models.vegetacion.No_Frutales import NoFrutal
from models.utils.Types_Enum import Tipo_Terreno


class Secuoya(NoFrutal):
    def __init__(self):
        super().__init__(
            especie="Secuoya",
            peso=10,
            max_peso=10,
            edad=49,
            edad_adulta=50,
            alcance=5,
            habitat=[Tipo_Terreno.SABANA]
        )
