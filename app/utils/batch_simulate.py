import csv
import numpy as np

from app.utils.simulacion import Simulacion


def batch_simulate(
        n_simulations,
        tamano_entorno=10,
        n_humanos=10,
        n_ciclos=100,
        genotipo_input={},
        dinosaurios=[],
        reproduccion=True,
        entorno=None,
        save_results=False,
        clima=None
):
    batch_poblacion = []

    for i in range(n_simulations): 
        if genotipo_input == {}:
            genotipo = {
                'fuerza': np.random.randint(5, 100),
                'velocidad': np.random.randint(5, 100),
                'resistencia': np.random.randint(5, 100),
                'inteligencia': np.random.randint(5, 100),
                'adaptabilidad': np.random.randint(5, 100),
                'supervivencia': np.random.randint(5, 100),
            }
        else:
            genotipo = genotipo_input.copy()

        simulacion = Simulacion(
            tamano_entorno=tamano_entorno,
            n_humanos=n_humanos,
            n_ciclos=n_ciclos,
            genotipo=genotipo,
            reproduccion=reproduccion,
            dinosaurios=dinosaurios,
            entorno=entorno,
            save_results=save_results,
            clima=clima
        )
        
        results = simulacion.ejecutar()
        batch_poblacion.append(results)
    
    return batch_poblacion


def exportar_resultados(archivo_csv, batch_poblacion):

    with open(archivo_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Escribir cabeceras
        writer.writerow(batch_poblacion[0].keys())
        
        for resultados in batch_poblacion:
            writer.writerow([
                resultados['duracion_supervivencia'],
                resultados['poblacion_inicial'],
                resultados['poblacion_total'],
                resultados['supervivencia_max'],
                resultados['edad_promedio'],
                resultados['salud_promedio'],
                resultados['clima'],
                resultados['terreno'],
                resultados['genotipo_fuerza'],
                resultados['genotipo_velocidad'],
                resultados['genotipo_resistencia'],
                resultados['genotipo_inteligencia'],
                resultados['genotipo_adaptabilidad'],
                resultados['genotipo_supervivencia'],
            ])
