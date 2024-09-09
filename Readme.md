# Jurasic Park Simulation

## Integrantes

- Daniel Ángel Arró Moreno
- Pedro Pablo Álvarez Portelles
- Abel Llerena Domingo 

## Introducción

Este proyecto consiste en una simulación basada en agentes discretos que modelan la supervivencia de un grupo de humanos en un entorno hostil inspirado en un parque jurásico. La simulación incorpora elementos de inteligencia artificial para encontrar mediante un algoritmo genético la mejor distribucion de características genéticas que permiten una mayor tasa de supervivencia humana en un ecosistema dinámico y complejo.

## Objetivos

1. Modelar la interacción entre humanos y dinosaurios en un entorno controlado.
2. Simular la adaptación y evolución de los agentes humanos a lo largo del tiempo.
3. Analizar estrategias de supervivencia y comportamientos emergentes.
4. Estudiar el impacto de diferentes variables ambientales en la supervivencia de los agentes.

## Componentes del Sistema

### 1. Entorno

- Mapa 2D de 20x20 casillas.
- Tipos de terreno: sabana, desierto, pantano, pradera, agua, acantilado.
- Condiciones climáticas variables (soleado, tormenta, lluvioso).
- Recursos limitados (comida, agua).

### 2. Agentes Humanos

- Atributos: salud, hambre, sed, cansancio, edad, género.
- Genotipos: fuerza, velocidad, resistencia, inteligencia, adaptabilidad, supervivencia.
- Acciones: desplazarse, interaccion_dinosaurio, buscar_agua, reproducirse, cazar.

### 3. Dinosaurios

- Diferentes especies con comportamientos únicos.
- Atributos: ataque, defensa, alimentacion, convivencia, habitats.

## Mecánicas de Simulación

### Ciclo de Vida de los Agentes Humanos

1. Actualización de estados fisiológicos.
2. Toma de decisiones basada en necesidades y entorno.
3. Ejecución de acciones.
4. Interacción con otros agentes y el entorno.
5. Reproducción y evolución genética.

### Interacción Humano-Dinosaurio

- Sistema de combate basado en atributos de ambos agentes.

En dependencia de la cantidad de dinosaurios y humanos generados en una casilla determinada, se determina quien gana en un enfrentamiento entre ambos bandos. En caso de que ganen los dinosaurios se registran las muertes de los agentes humanos.

### Sistema de Evolución

- Herencia de atributos genéticos.
- Mutaciones aleatorias durante la reproducción.

## Implementación Técnica

### Lenguaje y Bibliotecas

- Python 3.8+
- NumPy para cálculos numéricos eficientes.
- Matplotlib para visualización de datos y animaciones.

### Estructura del Código

1. `jurasic-simulation.ipynb`: Punto de entrada de la simulación.
2. `app/data/mapa.json`: Guarda la información por defecto de un mapa generado.
3. `app/models/entorno.py`: Definición y gestión del mapa y recursos.
4. `app/models/comunidad.py`: Clase y lógica para los agentes humanos.
5. `app/models/dinosaurio.py`: Clase y comportamientos de los dinosaurios.
6. `app/utils/simulacion.py`: Motor principal de la simulación.
7. `app/utils/batch_simulate.py`: Permite ejecutar varios ciclos de simulaciones.
8. `app/utils/draw_map.py`: Permite dibujar el mapa.
9. `app/utils/genetic_algorithm.py`: Clase y configuraciones para la ejecución del algoritmo genético.

## Análisis y Resultados

- Gráficos de población a lo largo del tiempo.
- Estadísticas de evolución genética.
- Patrones de comportamiento emergentes.

## Conclusiones y Trabajo Futuro

- Resumen de hallazgos principales.
- Discusión sobre la validez del modelo y sus limitaciones.
- Propuestas para mejoras y expansiones del proyecto.

## Modelo Matemático

[Documento de modelos matemáticos utilizados](docs/Modelo_matematico.md)

## Referencias

1. [Simulación basada en agentes](https://en.wikipedia.org/wiki/Agent-based_model)
2. [Teoría de la evolución](https://en.wikipedia.org/wiki/Evolution)
3. [Ecología de poblaciones](https://en.wikipedia.org/wiki/Population_ecology)

---

Este proyecto combina elementos de simulación computacional, inteligencia artificial y biología evolutiva para crear un modelo complejo y fascinante de supervivencia en un entorno hostil. A través de la observación y análisis de esta simulación, podemos obtener datos sobre comportamientoshumanos en un territorio jurásico, así como las características genéticas ás propicias para poder sobrevivir en comunidad en éste entorno.
