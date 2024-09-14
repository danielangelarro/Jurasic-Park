import numpy as np

from app.utils.simulacion import Simulacion


class CombinacionGenetica:
    def __init__(
            self,
            genotipo=None,
            tamano_entorno = 10,
            n_humanos = 10,
            n_ciclos = 100,
            reproduccion = True,
            dinosaurios = [],
            entorno = None,
    ):

        self.simulacion = Simulacion(
            tamano_entorno=tamano_entorno,
            n_humanos=n_humanos,
            n_ciclos=n_ciclos,
            genotipo=genotipo,
            reproduccion=reproduccion,
            dinosaurios=dinosaurios,
            entorno=entorno
        )
        self.genotipo = genotipo
        self.resultado = self.simulacion.ejecutar()
        self.aptitud = self.resultado["poblacion"][-1]
        self.max_poblacion = max(self.resultado["poblacion"])

    def __str__(self):
        return f"({self.genotipo})"


class GeneticAlgorithm:
    def __init__(self,
                 tamano_entorno=10,
                 n_humanos=10,
                 n_ciclos=100,
                 n_generaciones=50,
                 reproduccion=True,
                 dinosaurios=[],
                 entorno=None,
                 ):
        self.entorno = entorno
        self.tamano_entorno = tamano_entorno
        self.n_humanos = n_humanos
        self.n_ciclos = n_ciclos
        self.n_generaciones = n_generaciones
        self.reproduccion = reproduccion
        self.dinosaurios = dinosaurios

        self.poblacion = self.crear_poblacion()

    def crear_combinacion_genetica(self, genotipo=None):
        return CombinacionGenetica(
            genotipo=genotipo,
            tamano_entorno=self.tamano_entorno,
            n_humanos=self.n_humanos,
            n_ciclos=self.n_ciclos,
            reproduccion=self.reproduccion,
            dinosaurios=self.dinosaurios,
            entorno=self.entorno,
        )

    def crear_poblacion(self):
        return [self.crear_combinacion_genetica() for _ in range(10)]

    def seleccion(self):
        self.poblacion.sort(key=lambda x: (x.aptitud, x.max_poblacion), reverse=True)

    def crossover(self, padre: dict, madre: dict):
        genotipo_hijo1 = {
            "fuerza": 0,
            "velocidad": 0,
            "resistencia": 0,
            "inteligencia": 0,
            "adaptabilidad": 0,
            "supervivencia": 0
        }

        genotipo_hijo2 = {
            "fuerza": 0,
            "velocidad": 0,
            "resistencia": 0,
            "inteligencia": 0,
            "adaptabilidad": 0,
            "supervivencia": 0
        }

        for key in padre.keys():
            if np.random.rand() > 0.5:
                genotipo_hijo1[key] = padre[key]
                genotipo_hijo2[key] = madre[key]
            else:
                genotipo_hijo1[key] = madre[key]
                genotipo_hijo2[key] = padre[key]

        return genotipo_hijo1, genotipo_hijo2

    def mutacion(self, genotipo: dict, tasa_mutacion=0.1):
        for key in genotipo.keys():
            if np.random.rand() < tasa_mutacion:
                genotipo[key] += np.random.randint(-5, 5)
                genotipo[key] = max(0, min(100, genotipo[key]))

        return genotipo

    def evolucionar(self):
        for _ in range(self.n_generaciones):
            self.seleccion()

            nueva_poblacion = []
            for i in range(0, len(self.poblacion), 2):
                padre, madre = self.poblacion[i], self.poblacion[i + 1]
                hijo1, hijo2 = self.crossover(padre.genotipo, madre.genotipo)
                self.mutacion(hijo1)
                self.mutacion(hijo2)
                nueva_poblacion.extend([
                    self.crear_combinacion_genetica(hijo1),
                    self.crear_combinacion_genetica(hijo2)
                ])

            self.poblacion = nueva_poblacion.copy()
