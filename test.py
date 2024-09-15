import json
import numpy as np
import matplotlib.pyplot as plt

from app.utils.simulacion import Simulacion
from app.models.dinosaurios import *
from app.models.entorno import Entorno
from app.utils.draw_map import dibujar_mapa
from app.utils.batch_simulate import batch_simulate
from app.utils.genetic_algorithm import GeneticAlgorithm


with open('app/data/mapa.json', 'r') as file:
    mapa_data = json.load(file)



import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos desde el archivo CSV
datos = pd.read_csv('resultados_simulacion.csv')

# Convertir los valores de genotipo y habilidades en columnas separadas
# Aquí se asume que genotipo y habilidades están en formato de lista o JSON en el CSV

# Ejemplo de transformación para genotipo
genotipo_df = pd.json_normalize(datos['genotipo'].apply(pd.eval))
habilidades_df = pd.json_normalize(datos['habilidades'].apply(pd.eval))

# Concatenar con los datos principales
datos_completos = pd.concat([datos.drop(['genotipo', 'habilidades'], axis=1), genotipo_df, habilidades_df], axis=1)

# Análisis de hipótesis

# 1. Evaluar la influencia de la genética y habilidades en la supervivencia
sns.pairplot(datos_completos, vars=['supervivencia'] + list(genotipo_df.columns) + list(habilidades_df.columns))
plt.title('Influencia de Genética y Habilidades en la Supervivencia')
plt.show()

# 2. Evaluar cómo la adaptabilidad mejora la supervivencia
sns.lineplot(data=datos_completos, x='ciclo', y='supervivencia', hue='adaptabilidad')
plt.title('Adaptabilidad vs Supervivencia a lo largo de los ciclos')
plt.xlabel('Ciclo')
plt.ylabel('Supervivencia')
plt.show()

# 3. Evaluar qué variables aportan más peso a la supervivencia
correlaciones = datos_completos.corr()
sns.heatmap(correlaciones[['supervivencia']], annot=True, cmap='coolwarm')
plt.title('Correlaciones con Supervivencia')
plt.show()

# 4. Edad promedio de vida de los humanos
print(f'Edad promedio de vida de los humanos: {datos_completos["edad_promedio"].mean()}')

# 5. Impacto del clima y terreno en la supervivencia y toma de decisiones
sns.scatterplot(data=datos_completos, x='clima', y='supervivencia', hue='terreno')
plt.title('Clima vs Supervivencia')
plt.xlabel('Clima')
plt.ylabel('Supervivencia')
plt.show()

sns.scatterplot(data=datos_completos, x='terreno', y='supervivencia', hue='clima')
plt.title('Terreno vs Supervivencia')
plt.xlabel('Terreno')
plt.ylabel('Supervivencia')
plt.show()
