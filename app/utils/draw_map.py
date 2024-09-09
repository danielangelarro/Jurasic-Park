import json
import matplotlib.pyplot as plt
import numpy as np

def cargar_mapa(archivo='mapa.json'):
    with open(archivo, 'r') as file:
        return json.load(file)

def dibujar_mapa(mapa):
    terreno = mapa['terreno']
    tamaño = mapa['tamanio']

    # Definir colores para cada tipo de terreno
    colores = {
        'sabana': '#C2B280',    # Beige
        'desierto': '#FDD017',  # Amarillo arena
        'pantano': '#4A7023',   # Verde oscuro
        'pradera': '#7CFC00',   # Verde lima
        'agua': '#4169E1',      # Azul real
        'acantilado': '#8B4513' # Marrón
    }

    # Crear una matriz numérica para el mapa
    mapa_numerico = np.zeros((tamaño, tamaño))
    tipos_terreno = list(colores.keys())
    for i in range(tamaño):
        for j in range(tamaño):
            mapa_numerico[i, j] = tipos_terreno.index(terreno[i][j])

    # Crear la figura y el eje
    fig, ax = plt.subplots(figsize=(12, 10))

    # Dibujar el mapa
    im = ax.imshow(mapa_numerico, cmap=plt.cm.colors.ListedColormap(list(colores.values())))

    # Configurar los ticks
    ax.set_xticks(np.arange(-.5, tamaño, 1), minor=True)
    ax.set_yticks(np.arange(-.5, tamaño, 1), minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", size=0)
    ax.set_xticks(np.arange(0, tamaño, 1))
    ax.set_yticks(np.arange(0, tamaño, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Crear la leyenda
    patches = [plt.Rectangle((0,0),1,1, facecolor=color, edgecolor='none') for color in colores.values()]
    plt.legend(patches, colores.keys(), loc='center left', bbox_to_anchor=(1, 0.5))

    # Añadir título
    plt.title('Mapa del Terreno', fontsize=16)

    # Ajustar el diseño y mostrar
    plt.tight_layout()
    plt.show()

# Cargar y dibujar el mapa
mapa = cargar_mapa()
dibujar_mapa(mapa)