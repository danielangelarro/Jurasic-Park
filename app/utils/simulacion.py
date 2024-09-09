import numpy as np

from app.models.comunidad import Comunidad
from app.models.entorno import Entorno


class Simulacion:
    def __init__(self,
        tamano_entorno=10,
        n_humanos=10,
        n_ciclos=100,
        genotipo={},
        reproduccion=True,
        dinosaurios=[],
        entorno=None,
    ):
        self.entorno = entorno if entorno is not None else Entorno(tamano_entorno)
        self.comunidad = Comunidad(n_humanos, tamano_entorno)
        self.n_ciclos = n_ciclos
        self.reproduccion = reproduccion
        self.dinosaurios = dinosaurios

        for key in genotipo:
            self.comunidad.__dict__[f'genotipo_{key}'] = np.full(10, genotipo[key])

    def ejecutar(self):
        resultados = {'ciclo': [], 'poblacion': [], 'clima': [], 'muerte_dinosaurios': []}

        for ciclo in range(self.n_ciclos):
            self.entorno.cambiar_clima()
            self.comunidad.actualizar_estados_fisiologicos()
            self.comunidad.mortalidad()

            self.comunidad.desplazarse()

            dinosaurios_posicion = self.entorno.generate_dinosaurios(posiciones=self.comunidad.posiciones)
            dinosaurios_resultado = self.comunidad.interaccion_dinosaurio(dinoasurios_por_posicion=dinosaurios_posicion)

            agua_resultado = self.comunidad.buscar_agua(self.entorno)
            caza_resultado = self.comunidad.cazar(self.entorno)
            nacimientos = self.comunidad.reproducirse() if self.reproduccion else 0

            resultados['ciclo'].append(ciclo)
            resultados['poblacion'].append(self.comunidad.n_humanos)
            resultados['clima'].append(self.entorno.clima)
            resultados['muerte_dinosaurios'].append(dinosaurios_resultado)

        return resultados
