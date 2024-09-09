import numpy as np
from app.models.convivencia_type import ConvivenciaType


# Configuracion inicial
CLIMA_ESTADOS = ['soleado', 'tormenta', 'lluvioso']
TERRENO_TIPOS = ['sabana', 'desierto', 'pantano', 'pradera', 'agua', 'acantilado']


# Matriz de transicion de clima
MATRIZ_CLIMA = np.array([
    [0.7, 0.2, 0.1],  # Soleado
    [0.3, 0.4, 0.3],  # Tormenta
    [0.4, 0.3, 0.3]  # Lluvioso
])


class Entorno:
    def __init__(self, tamano=10, terreno=None):
        self.tamano = tamano
        self.terreno = terreno if terreno is not None else np.random.choice(TERRENO_TIPOS, (tamano, tamano))
        self.clima = 'soleado'
        self.tipos_dinosaurios = []

    def add_tipos_dinosaurios(self, tipos_dinosaurios):
        self.tipos_dinosaurios = [dino() for dino in tipos_dinosaurios]

    def cambiar_clima(self):
        estado_actual = CLIMA_ESTADOS.index(self.clima)
        self.clima = np.random.choice(CLIMA_ESTADOS, p=MATRIZ_CLIMA[estado_actual])

    def probabilidad_buscar_agua(self, tipo_terreno):
        # Diccionario de probabilidades basado en el tipo de terreno
        probabilidad_terreno = {
            'sabana': 0.7,
            'desierto': 0.9,
            'pantano': 0.3,
            'pradera': 0.2,
            'agua': 0.1,
            'acantilado': 0.4,
        }

        # Diccionario de probabilidades basado en el estado del clima
        probabilidad_clima = {
            'soleado': 0.8,
            'tormenta': 0.5,
            'lluvioso': 0.1,
        }

        # Combinar probabilidades
        probabilidad = probabilidad_terreno[tipo_terreno] * probabilidad_clima[self.clima]

        return probabilidad

    def probabilidad_cazar(self, tipo_terreno):
        # Diccionario de probabilidades basadas en el tipo de terreno
        probabilidad_terreno = {
            'sabana': 0.5,
            'desierto': 0.8,
            'pantano': 0.4,
            'pradera': 0.2,
            'agua': 0.1,
            'acantilado': 0.3,
        }

        # Diccionario de probabilidades basadas en el estado del clima
        probabilidad_clima = {
            'soleado': 0.7,
            'tormenta': 0.3,
            'lluvioso': 0.2,
        }

        # Calcular la probabilidad final como el producto de las probabilidades individuales
        probabilidad_final = probabilidad_terreno[tipo_terreno] * probabilidad_clima[self.clima]

        return probabilidad_final

    def generate_dinosaurios(self, posiciones):
        dinosaurios_en_terreno = {}

        for posicion in posiciones:
            posicion = tuple(posicion)
            terreno = self.terreno[posicion[0], posicion[1]]
            dinosaurios_en_terreno[posicion] = {'ataque': 0, 'defensa': 0}

            dinos = list(filter(lambda d: terreno in d.habitat, self.tipos_dinosaurios))
            dinos.sort(key=lambda d: d.probabilidad_aparicion(self.clima, terreno), reverse=True)

            for dino in dinos:
                cantidad = np.random.randint(2) if dino.convivencia == ConvivenciaType.SOLITARIO else np.random.randint(
                    4)
                dinosaurios_en_terreno[posicion]['ataque'] += cantidad * dino.ataque

        return dinosaurios_en_terreno
