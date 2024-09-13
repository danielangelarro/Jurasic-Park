import json
import numpy as np
import matplotlib.pyplot as plt

from app.models.dinosaurios import *
from app.models.entorno import Entorno
from app.utils.draw_map import dibujar_mapa
from app.utils.batch_simulate import batch_simulate
from app.utils.genetic_algorithm import GeneticAlgorithm


with open('app/data/mapa.json', 'r') as file:
    mapa_data = json.load(file)


def batch_simulate_genotipos(n_simulaciones, dinosaurios=[], reproduccion=True):
    resultados_batch = []

    # Diferentes configuraciones de genotipos para evaluar
    genotipos_config = [
        {'fuerza': 80, 'inteligencia': 50, 'resistencia': 60},  # Humanos fuertes
        {'fuerza': 50, 'inteligencia': 90, 'resistencia': 70},  # Humanos inteligentes
        {'fuerza': 70, 'inteligencia': 70, 'resistencia': 70},  # Humanos balanceados
        {'fuerza': 30, 'inteligencia': 40, 'resistencia': 90},  # Humanos resistentes
    ]

    entorno = Entorno(mapa_data['tamanio'], np.matrix(mapa_data['terreno']))

    for genotipo in genotipos_config:
        poblacion_final = []

        results = batch_simulate(
            n_simulations=n_simulaciones,
            genotipo=genotipo,
            dinosaurios=dinosaurios,
            reproduccion=reproduccion,
            entorno=entorno
        )

        for i, result in enumerate(results):
            poblacion_final.append(result['poblacion'][-1])  # Población al final de la simulación

        # Guardar los resultados de cada configuración de genotipo
        resultados_batch.append({
            'genotipo': genotipo,
            'poblacion': result['poblacion'],
            'results': results,
            'poblacion_final': np.mean(poblacion_final)
        })

    return resultados_batch


def visualizar_resultados_batch(resultados_batch):
    # Extraer la información para graficar
    genotipos = ["Humanos fuertes", "Humanos inteligentes", "Humanos balanceados", "Humanos resistentes"]
    poblacion_final = [r['poblacion_final'] for r in resultados_batch]

    # Crear gráfico de barras para visualizar la hipótesis
    plt.figure(figsize=(10, 6))
    plt.bar(genotipos, poblacion_final)
    plt.title('Efecto de Genotipos en la Supervivencia')
    plt.xlabel('Genotipo (Fuerza, Inteligencia, Resistencia)')
    plt.ylabel('Población Final Promedio')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# Ejecutar simulacion sin dinosaurios
resultados_batch = batch_simulate_genotipos(
    n_simulaciones=50,
)

# Visualizar los resultados
visualizar_resultados_batch(resultados_batch)
