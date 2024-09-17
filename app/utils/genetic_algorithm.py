import numpy as np
from app.utils.simulacion import Simulacion

class CombinacionGenetica:
    def __init__(self, genotipo={}, tamano_entorno=10, n_humanos=10, n_ciclos=100, reproduccion=True, dinosaurios=[], entorno=None):
        if genotipo == {}:
            genotipo = self.generar_genotipo_aleatorio()

        self.simulacion = Simulacion(
            tamano_entorno=tamano_entorno,
            n_humanos=n_humanos,
            n_ciclos=n_ciclos,
            genotipo=genotipo,
            reproduccion=reproduccion,
            dinosaurios=dinosaurios,
            entorno=entorno,
            save_results=True
        )
        self.genotipo = genotipo.copy()
        self.resultado = self.simulacion.ejecutar()
        self.aptitud = self.resultado["duracion_supervivencia"]
        self.max_poblacion = self.resultado["poblacion_total"]

    def generar_genotipo_aleatorio(self):
        return {
            'fuerza': np.random.randint(5, 100),
            'velocidad': np.random.randint(5, 100),
            'resistencia': np.random.randint(5, 100),
            'inteligencia': np.random.randint(5, 100),
            'adaptabilidad': np.random.randint(5, 100),
            'supervivencia': np.random.randint(5, 100)
        }

    def __str__(self):
        return f"({self.genotipo})"


class GeneticAlgorithm:
    def __init__(
            self, 
            tamano_entorno=10, 
            n_humanos=10, 
            n_ciclos=100, 
            n_generaciones=500, 
            n_poblacion=50, 
            reproduccion=True, 
            dinosaurios=[], 
            entorno=None, 
            tasa_mutacion_inicial=0.1, 
            elitismo=0.05
        ):
        self.entorno = entorno
        self.tamano_entorno = tamano_entorno
        self.n_humanos = n_humanos
        self.n_ciclos = n_ciclos
        self.n_generaciones = n_generaciones
        self.n_poblacion = n_poblacion
        self.reproduccion = reproduccion
        self.dinosaurios = dinosaurios
        self.tasa_mutacion_inicial = tasa_mutacion_inicial
        self.elitismo = elitismo
        self.poblacion = self.crear_poblacion()

    def crear_combinacion_genetica(self, genotipo={}):
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
        return [self.crear_combinacion_genetica() for _ in range(self.n_poblacion)]

    def seleccion(self):
        self.poblacion.sort(key=lambda x: (x.aptitud, x.max_poblacion), reverse=True)

    def crossover(self, padre: dict, madre: dict):
        # Utilizando crossover de un solo punto
        punto_corte = np.random.randint(1, len(padre))
        hijo1 = {**padre}
        hijo2 = {**madre}
        for key in list(padre.keys())[punto_corte:]:
            hijo1[key], hijo2[key] = madre[key], padre[key]
        return hijo1, hijo2

    def mutacion(self, genotipo: dict, tasa_mutacion_actual):
        # Mutación con tasa adaptativa
        for key in genotipo.keys():
            if np.random.rand() < tasa_mutacion_actual:
                genotipo[key] += np.random.normal(loc=0, scale=5)
                genotipo[key] = max(5, min(100, genotipo[key]))
        return genotipo

    def evolucionar(self):
        historial_poblacion = []
        
        for generacion in range(self.n_generaciones):
            self.seleccion()
            elite_count = int(self.elitismo * len(self.poblacion))
            nueva_poblacion = self.poblacion[:elite_count]  # Preservamos a los mejores individuos (elitismo)

            # Adaptación de tasa de mutación para mantener diversidad
            tasa_mutacion_actual = self.tasa_mutacion_inicial * (1 - generacion / self.n_generaciones)
            
            while len(nueva_poblacion) < self.n_poblacion:
                # Selección de padres aleatoria (torneo)
                padre, madre = np.random.choice(self.poblacion[:10], 2)
                hijo1, hijo2 = self.crossover(padre.genotipo, madre.genotipo)
                hijo1 = self.mutacion(hijo1, tasa_mutacion_actual)
                hijo2 = self.mutacion(hijo2, tasa_mutacion_actual)
                nueva_poblacion.extend([
                    self.crear_combinacion_genetica(hijo1),
                    self.crear_combinacion_genetica(hijo2)
                ])

            self.poblacion = nueva_poblacion.copy()
            historial_poblacion.append(self.poblacion[0].aptitud)

        return historial_poblacion
