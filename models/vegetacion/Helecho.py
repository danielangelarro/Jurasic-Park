from models.vegetacion.No_Frutales import NoFrutal
from models.utils.Types_Enum import Tipo_Terreno


class Helecho(NoFrutal):
    def __init__(self):
        super().__init__(
            especie="Helecho",
            peso=1,
            max_peso=1,
            edad=10,
            edad_adulta=5,
            alcance=5,
            habitat=[Tipo_Terreno.SABANA]
        )