import pandas as pd
import numpy as np

from app.models.comunidad import Comunidad
from app.models.entorno import Entorno
from app.utils.ia.expert_system import SistemaExperto
from app.utils.ia.expert_system import EstadoComunidad


class Simulacion:
    def __init__(self,
        tamano_entorno=10,
        n_humanos=10,
        n_ciclos=100,
        genotipo={},
        reproduccion=True,
        dinosaurios=[],
        entorno=None,
        save_results=False,
        clima=None,
    ):
        self.entorno = entorno if entorno is not None else Entorno(tamano_entorno)
        self.comunidad = Comunidad(n_humanos, tamano_entorno)
        self.n_ciclos = n_ciclos
        self.reproduccion = reproduccion
        self.dinosaurios = dinosaurios
        self.save_results = save_results
        self.clima = clima

        if clima is not None:
            self.entorno.clima = clima

        for key in genotipo:
            self.comunidad.__dict__[f'genotipo_{key}'] = np.full(n_humanos, genotipo[key])

        # Inicializamos el sistema experto con la comunidad y el entorno
        self.sistema_experto = SistemaExperto(comunidad=self.comunidad, entorno=self.entorno)

    def ejecutar(self):
        resultados = {
            'duracion_supervivencia': 0,
            'poblacion_inicial': self.comunidad.n_humanos,
            'poblacion_total': 0, 
            'supervivencia_max': 0, 
            'edad_promedio': 0,
            'salud_promedio': 0,
            'clima': "", 
            'terreno': "",
            'genotipo_fuerza': np.mean(self.comunidad.genotipo_fuerza),
            'genotipo_velocidad': np.mean(self.comunidad.genotipo_velocidad),
            'genotipo_resistencia': np.mean(self.comunidad.genotipo_resistencia),
            'genotipo_inteligencia': np.mean(self.comunidad.genotipo_inteligencia),
            'genotipo_adaptabilidad': np.mean(self.comunidad.genotipo_adaptabilidad),
            'genotipo_supervivencia': np.mean(self.comunidad.genotipo_supervivencia),
        }
        
        clima, terrenos = set(), set()

        for ciclo in range(self.n_ciclos):
            if self.clima is None:
                self.entorno.cambiar_clima()
            
            self.comunidad.actualizar_estados_fisiologicos()
            self.comunidad.mortalidad()

            clima.add(self.entorno.clima)
            
            for i in range(self.comunidad.n_humanos):
                tipo_terreno = self.entorno.terreno[self.comunidad.posiciones[i][0], self.comunidad.posiciones[i][1]]
                terrenos.add(tipo_terreno)

            self.comunidad.desplazarse()

            dinosaurios_posicion = self.entorno.generate_dinosaurios(posiciones=self.comunidad.posiciones)
            dinosaurios_resultado = self.comunidad.interaccion_dinosaurio(dinoasurios_por_posicion=dinosaurios_posicion)

            self.sistema_experto.reset()
            self.sistema_experto.declare(EstadoComunidad(sed=np.mean(self.comunidad.sed)))
            self.sistema_experto.declare(EstadoComunidad(hambre=np.mean(self.comunidad.hambre)))
            self.sistema_experto.declare(EstadoComunidad(cansancio=np.mean(self.comunidad.cansancio)))
            self.sistema_experto.declare(EstadoComunidad(permitir_reproduccion=self.reproduccion))
            self.sistema_experto.run()
            
            if self.save_results and self.comunidad.n_humanos == 0:
                break
            
            resultados['duracion_supervivencia'] = ciclo + 1

        # Recolectar datos para cada ciclo
        resultados['poblacion_total'] = self.comunidad.poblacion_total
        resultados['supervivencia_max'] = self.comunidad.supervivencia_max
        resultados['edad_promedio'] = np.mean(np.concatenate((self.comunidad.edad_final, self.comunidad.edad)))
        resultados['salud_promedio'] = np.mean(np.concatenate((self.comunidad.salud_final, self.comunidad.salud)))
        resultados['clima'] = str(clima)
        resultados['terreno'] = str(terrenos)
        
        return resultados
