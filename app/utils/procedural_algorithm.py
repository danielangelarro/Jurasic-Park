import numpy as np
import matplotlib.pyplot as plt
from noise import snoise2
import random
import json


def generate_map(size=20, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # Definir tipos de terreno y sus umbrales
    terrain_types = ['agua', 'pantano', 'pradera', 'sabana', 'desierto', 'acantilado']
    thresholds = [-0.3, -0.1, 0.1, 0.3, 0.5, 0.7]

    # Generar mapa base con ruido de Perlin
    scale = 5.0
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0

    world = np.zeros((size, size))
    for y in range(size):
        for x in range(size):
            world[y][x] = snoise2(x / scale,
                                  y / scale,
                                  octaves=octaves,
                                  persistence=persistence,
                                  lacunarity=lacunarity,
                                  repeatx=size,
                                  repeaty=size,
                                  base=seed if seed else 0)

    # Convertir valores de ruido a tipos de terreno
    terrain_map = []
    for row in world:
        terrain_row = []
        for value in row:
            for i, threshold in enumerate(thresholds):
                if value < threshold:
                    terrain_row.append(terrain_types[i])
                    break
            else:
                terrain_row.append(terrain_types[-1])
        terrain_map.append(terrain_row)

    return {"tamanio": size, "terreno": terrain_map}


def save_map_to_json(map_data, filename="generated_map.json"):
    with open(filename, 'w') as f:
        json.dump(map_data, f)


def draw_map(map_data, seed=None):
    terrain = map_data['terreno']
    size = map_data['tamanio']

    colors = {
        'agua': '#4169E1',  # Azul real
        'pantano': '#4A7023',  # Verde oscuro
        'pradera': '#7CFC00',  # Verde lima
        'sabana': '#C2B280',  # Beige
        'desierto': '#FDD017',  # Amarillo arena
        'acantilado': '#8B4513'  # Marrón
    }

    terrain_types = list(colors.keys())
    numeric_map = np.array([[terrain_types.index(cell) for cell in row] for row in terrain])

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(numeric_map, cmap=plt.cm.colors.ListedColormap(list(colors.values())))

    ax.set_xticks(np.arange(-.5, size, 1), minor=True)
    ax.set_yticks(np.arange(-.5, size, 1), minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", size=0)
    ax.set_xticks([])
    ax.set_yticks([])

    patches = [plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor='none') for color in colors.values()]
    plt.legend(patches, colors.keys(), loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(f'Mapa Generado (Semilla: {seed})', fontsize=16)
    plt.tight_layout()
    plt.show()


# Generar y dibujar varios mapas
def procedural_algorithm_for_generate_map(seeds=[]):
    for seed in seeds:
        map_data = generate_map(size=50, seed=seed)
        save_map_to_json(map_data, f"./app/data/map_seed_{seed}.json")
        draw_map(map_data, seed)
