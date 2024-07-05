from models.vegetacion.Vegetacion import Vegetacion


class NoFrutal(Vegetacion):
    def __init__(self, especie, peso, max_peso, edad, edad_adulta, alcance, habitat):
        super().__init__(especie, False, peso, max_peso, edad, edad_adulta, alcance, habitat)