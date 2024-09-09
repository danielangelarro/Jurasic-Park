class Dinosaurio:
    def __init__(self, tipo, alimentacion, convivencia, ataque, defensa, habitat):
        self.tipo = tipo
        self.alimentacion = alimentacion
        self.convivencia = convivencia
        self.ataque = ataque
        self.defensa = defensa
        self.habitats = habitat

    def is_habitat(self, terreno):
        return terreno in self.habitats


class Braquiosaurio(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.7,
            'tormenta': 0.2,
            'lluvioso': 0.5,
        }

        probabilidad_terreno = {
            'sabana': 0.6,
            'pradera': 0.8,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Triceratops(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'pantano']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.6,
            'tormenta': 0.3,
            'lluvioso': 0.5,
        }

        probabilidad_terreno = {
            'sabana': 0.7,
            'pradera': 0.8,
            'pantano': 0.4,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Pteranodonte(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['acantilado', 'agua', 'sabana']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.8,
            'tormenta': 0.1,
            'lluvioso': 0.3,
        }

        probabilidad_terreno = {
            'acantilado': 0.7,
            'agua': 0.6,
            'sabana': 0.4,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Velociraptor(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'desierto']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.6,
            'tormenta': 0.4,
            'lluvioso': 0.3,
        }

        probabilidad_terreno = {
            'sabana': 0.7,
            'pradera': 0.6,
            'desierto': 0.5,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class TiranosaurioRex(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'pantano']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.5,
            'tormenta': 0.4,
            'lluvioso': 0.6,
        }

        probabilidad_terreno = {
            'sabana': 0.7,
            'pradera': 0.6,
            'pantano': 0.5,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Carnotauro(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'desierto']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.7,
            'tormenta': 0.3,
            'lluvioso': 0.4,
        }

        probabilidad_terreno = {
            'sabana': 0.6,
            'pradera': 0.5,
            'desierto': 0.7,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Estegosaurio(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'pantano']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.6,
            'tormenta': 0.3,
            'lluvioso': 0.5,
        }

        probabilidad_terreno = {
            'sabana': 0.5,
            'pradera': 0.7,
            'pantano': 0.4,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Anquilosaurio(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'pantano']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.5,
            'tormenta': 0.4,
            'lluvioso': 0.6,
        }

        probabilidad_terreno = {
            'sabana': 0.6,
            'pradera': 0.7,
            'pantano': 0.5,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]


class Iguanodonte(Dinosaurio):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.habitats = ['sabana', 'pradera', 'pantano', 'desierto']

    def probabilidad_aparicion(self, clima, terreno):
        if not self.is_habitat(terreno):
            return 0

        probabilidad_clima = {
            'soleado': 0.6,
            'tormenta': 0.3,
            'lluvioso': 0.5,
        }

        probabilidad_terreno = {
            'sabana': 0.7,
            'pradera': 0.8,
            'pantano': 0.5,
            'desierto': 0.4,
        }

        return probabilidad_clima[clima] * probabilidad_terreno[terreno]
