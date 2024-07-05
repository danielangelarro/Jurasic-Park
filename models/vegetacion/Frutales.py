from models.vegetacion.Vegetacion import Vegetacion


class Frutal(Vegetacion):
    def __init__(self, especie, peso, max_peso, edad, edad_adulta, alcance, habitat):
        super().__init__(especie, True, peso, max_peso, edad, edad_adulta, alcance, habitat)
