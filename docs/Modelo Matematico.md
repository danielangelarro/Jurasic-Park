Para crear un modelo matemático completo para la simulación de un ecosistema con humanos y dinosaurios, podemos utilizar distribuciones probabilísticas para definir la probabilidad de que ocurran diversas acciones y eventos. Aquí está el modelo detallado, incluyendo la forma en que se utilizan las funciones de probabilidad estadísticas.

### 1. **Variables y Estados de la Simulación**

#### a. **Variables Globales**
- **Tiempo (t)**: Una variable discreta que avanza en intervalos. Influye en el clima y las necesidades fisiológicas.
- **Clima**: Modelado usando una cadena de Markov para transiciones entre estados climáticos (soleado, lluvioso, tormenta). La matriz de
transición se define como: [ $P( ext{clima}{t+1} = j | ext{clima}t = i) = M_{ij}$ ]
- **Terreno**: Matriz que define el tipo de terreno de cada celda (sabana, desierto, pantano, pradera, agua, acantilado)  y recursos disponibles (agua, alimentos). Estos recursos varían con el clima.

#### b. **Estados de los Agentes (Humanos y Dinosaurios)**
- **Fisiológicos**:
  - **Hambre (H)**: Escala de 0 a 100.
  - **Sed (S)**: Escala de 0 a 100.
  - **Cansancio (C)**: Escala de 0 a 100.
  - **Temperatura Corporal (TC)**: Escala de 0 a 100.
- **Edad (A)**: Influye en la capacidad de reproducirse y la expectativa de vida.
- **Salud (Sal)**: Escala de 0 a 100.
- **Área de Visión (AV)**: Determina qué entidades puede ver un agente.
- **Área de Acción (AA)**: Determina qué entidades puede interactuar un agente.

### 2. **Distribuciones Probabilísticas para Acciones y Eventos**

#### a. **Clima**
- **Cambio de Clima**: Probabilidad de cambio cada unidad de tiempo, usando cadenas de Markov.

| Estado Actual \ Próximo Estado | Soleado | Tormenta | Lluvioso |
|---------------------------------|---------|----------|----------|
| **Soleado**                     | 0.7     | 0.2      | 0.1      |
| **Tormenta**                    | 0.3     | 0.4      | 0.3      |
| **Lluvioso**                    | 0.4     | 0.3      | 0.3      |

### Explicación de la tabla:

1. **Soleado**:
   - Hay un 70% de probabilidad de que siga siendo soleado.
   - Hay un 20% de probabilidad de que pase a tormenta.
   - Hay un 10% de probabilidad de que pase a lluvioso.

2. **Tormenta**:
   - Hay un 30% de probabilidad de que pase a soleado.
   - Hay un 40% de probabilidad de que siga siendo tormenta.
   - Hay un 30% de probabilidad de que pase a lluvioso.

3. **Lluvioso**:
   - Hay un 40% de probabilidad de que pase a soleado.
   - Hay un 30% de probabilidad de que pase a tormenta.
   - Hay un 30% de probabilidad de que siga siendo lluvioso.

Esta tabla permite simular el clima día a día, partiendo de un estado inicial y utilizando las probabilidades para determinar el estado siguiente.

#### b. **Estados Fisiológicos**
- **Incremento de Hambre, Sed, y Cansancio**: El modelo matemático para las funciones de distribución logarítmica utilizadas para simular los índices de hambre, sed y cansancio en entidades humanas se basa en la función logarítmica.

1. Índice de Hambre
La función que modela el índice de hambre en función del tiempo \( t \) es:

\[
$H(t) = \min\left(\max\left(a_h \cdot \log(t + 1) + b_h, 0\right), 1\right)$
\]

Donde:
- \( H(t) \) es el índice de hambre en el tiempo \( t \), con \( 0 \leq H(t) \leq 1 \).
- \( a_h \) es un parámetro de escala que ajusta la pendiente de la curva logarítmica.
- \( b_h \) es un parámetro de desplazamiento que ajusta el valor inicial del índice.
- \( t \) es el tiempo transcurrido.

2. Índice de Sed
La función que modela el índice de sed en función del tiempo \( t \) es:

\[
$S(t) = \min\left(\max\left(a_s \cdot \log(t + 1) + b_s, 0\right), 1\right)$
\]

Donde:
- \( S(t) \) es el índice de sed en el tiempo \( t \), con \( 0 \leq S(t) \leq 1 \).
- \( a_s \) es un parámetro de escala que ajusta la pendiente de la curva logarítmica.
- \( b_s \) es un parámetro de desplazamiento que ajusta el valor inicial del índice.
- \( t \) es el tiempo transcurrido.

3. Índice de Cansancio
La función que modela el índice de cansancio en función del tiempo \( t \) es:

\[
C(t) = \min\left(\max\left(a_c \cdot \log(t + 1) + b_c, 0\right), 1\right)
\]

Donde:
- \( C(t) \) es el índice de cansancio en el tiempo \( t \), con \( 0 \leq C(t) \leq 1 \).
- \( a_c \) es un parámetro de escala que ajusta la pendiente de la curva logarítmica.
- \( b_c \) es un parámetro de desplazamiento que ajusta el valor inicial del índice.
- \( t \) es el tiempo transcurrido.

> [!NOTE]
> - **Logaritmo Natural**: El uso de \( \log(t + 1) \) es esencial para manejar situaciones en las que \( t = 0 \), evitando el logaritmo de cero que no está definido.
> - **Clipping**: Las funciones utilizan operadores de \(\max\) y \(\min\) para asegurar que los índices resultantes se mantengan dentro del rango [0, 1].
> - **Parámetros de Ajuste**: Los parámetros \( a_h \), \( a_s \), \( a_c \), \( b_h \), \( b_s \), \( b_c \) permiten ajustar las curvas para reflejar diferentes comportamientos fisiológicos de las entidades en la simulación.


```Interpretación:```
- A medida que pasa el tiempo, los índices de hambre, sed y cansancio aumentan de manera logarítmica. Inicialmente, estos incrementos son más rápidos, pero tienden a estabilizarse con el tiempo.
- Los valores de \( $a$ \) y \( $b$ \) permiten ajustar cuán rápidamente crecen estos índices y el punto de inicio en el tiempo.

Este modelo matemático proporciona una base para implementar simulaciones donde los estados de las entidades humanas cambian con el tiempo de acuerdo con las necesidades fisiológicas básicas.

### 3. **Acciones de los Agentes**

Cada acción tiene una probabilidad de selección basada en la necesidad (hambre, sed, cansancio) y una probabilidad de éxito basada en características genéticas, habilidades, terreno, y clima.

#### a. **Buscar Agua**
- **Probabilidad de Selección**: Proporcional al nivel de sed.
  \[
  $P(\text{selección}) = \frac{S}{100}$
  \]
- **Probabilidad de Éxito**: Depende del terreno y de la adaptabilidad.
  \[
  $P(\text{éxito}) = \text{base} + \text{terreno\_mod} + \text{adaptabilidad\_mod}$
  \]
  Con ajustes basados en terreno y características genéticas.

#### b. **Cazar**
- **Probabilidad de Selección**: Proporcional al nivel de hambre.
  \[
  $P(\text{selección}) = \frac{H}{100}$
  \]
- **Probabilidad de Éxito**: Depende de habilidades de caza, fuerza, velocidad, y terreno.
  \[
  $P(\text{éxito}) = \text{base} + \text{habilidad\_mod} + \text{fuerza\_mod} + \text{velocidad\_mod} + \text{terreno\_mod}$
  \]

#### c. **Reproducción**
- **Probabilidad de Selección**: Depende de la salud, edad, y la presencia de una pareja compatible.
  \[
  $P(\text{selección}) = \text{base} + \text{salud\_mod} + \text{edad\_mod} + \text{pareja\_mod}$
  \]
- **Probabilidad de Éxito**:
  \[
  $P(\text{éxito}) = \text{base} + \text{genetica\_mod}$
  \]

#### d. **Muerte**
- **Probabilidad de Muerte**: Aumenta con el nivel de hambre, sed, cansancio, y disminución de la salud.
  \[
  $P(\text{muerte}) = 1 - e^{-\lambda (H + S + C - Sal)}$
  \]

### 4. **Asignación de Funciones Probabilísticas a Acciones y Eventos**

#### a. **Distribuciones para la Probabilidad de Éxito**
- **Buscar Agua**:
  - **Probabilidad de Selección**:
  \[
  $P(\text{selección}) = \frac{S}{100} \times f(T, C)$
  \]
    Donde \( $f(T, C)$ \) es una función que ajusta la probabilidad según el terreno y el clima (p.ej., mayor en desiertos, menor en praderas).

  - **Probabilidad de Éxito**:
  \[
  $P(\text{éxito}) = \text{base} + \text{adaptabilidad\_mod} + g(T, C)$
  \]
    Donde \( $g(T, C)$ \) es una función que modifica la probabilidad según el terreno y el clima (p.ej., mayor en terrenos con agua, menor en terrenos áridos).


- **Cazar**:
  - **Probabilidad de Selección**:
  \[
  $P(\text{selección}) = \frac{H}{100} \times h(AV, C)$
  \]
    Donde \( $h(AV, C)$ \) ajusta la probabilidad según la visibilidad y las condiciones climáticas.

  - **Probabilidad de Éxito**:
  \[
  $P(\text{éxito}) = \text{base} + \text{habilidad\_mod} + \text{fuerza\_mod} + \text{terreno\_mod} + j(C)$
  \]
    Donde \( $j(C)$ \) es una función que modifica la probabilidad según las condiciones climáticas (p.ej., menor éxito en tormentas).

- **Reproducción**
  - **Probabilidad de Selección**:
  \[
  $P(\text{selección}) = k(Sal, A, \text{pareja\_mod})$
  \]
    Donde \( $k(Sal, A, \text{pareja\_mod})$ \) depende de la salud, edad, y compatibilidad de pareja.

  - **Probabilidad de Éxito**:
  \[
  $P(\text{éxito}) = \text{base} + \text{genetica\_mod} + m(C)$
  \]
    Donde \( m(C) \) modifica la probabilidad según el clima (p.ej., menor éxito en climas adversos).

- **Probabilidad de Muerte**:
  \[
  $P(\text{muerte}) = 1 - e^{-\lambda (H + S + C - Sal + TC)}$
  \]
    Donde \( $TC$ \) es la temperatura corporal afectada por el clima, que puede influir negativamente en la salud.

- **Recolectar**:
  \[
  $P(\text{éxito}) = \text{chisquare}(2) + \text{inteligencia\_mod}$
  \]
  La distribución chi-cuadrada puede reflejar la diversidad en la habilidad de recolección.

- **Descansar**:
  \[
  $P(\text{eficacia}) = \text{uniform}(0.2, 0.8) + \text{resistencia\_mod}$
  \]

- **Buscar Sombra**:
  - **Probabilidad de Éxito**:
  \[
  $P(\text{éxito}) = \text{uniform}(0.4, 0.9) + \text{adaptabilidad\_mod} + n(C)$
  \]
    Donde \( $n(C)$ \) aumenta la probabilidad si el clima es caluroso.

- **Escalar**:
  \[
  $P(\text{éxito}) = \text{uniform}(0.1, 0.7) + \text{fuerza\_mod} + \text{resistencia\_mod}$
  \]

- **Explorar**:
  - **Probabilidad de Éxito**:
  \[
  $P(\text{éxito}) = \text{chisquare}(1) + \text{inteligencia\_mod} + \text{adaptabilidad\_mod} + p(T)$
  \]
    Donde \( $p(T)$ \) modifica la probabilidad según el tipo de terreno.

- **Evitar Peligros**:
  \[
  $P(\text{éxito}) = \text{uniform}(0.5, 1.0) + \text{velocidad\_mod} + \text{inteligencia\_mod}$
  \]


### 5. **Implementacion de funciones auxiliares**

Para crear un modelo matemático que represente el valor de ataque y defensa basado en los parámetros dados, podemos considerar cómo cada factor contribuye a estas características. Aquí te propongo un modelo que toma en cuenta estos factores:

1. Valor de Ataque:

```python
def calcular_ataque(self, indice):
    base_ataque = self.genotipo_fuerza[indice] * 0.4 + self.genotipo_velocidad[indice] * 0.3 + self.genotipo_inteligencia[indice] * 0.2

    factor_salud = self.salud[indice] / 100
    factor_hambre = max(0, 1 - self.hambre[indice] / 100)
    factor_sed = max(0, 1 - self.sed[indice] / 100)
    factor_cansancio = max(0, 1 - self.cansancio[indice] / 100)
    factor_temperatura = max(0, 1 - abs(self.temperatura_corporal[indice] - 37) / 10)
    factor_edad = 1 - (self.edad[indice] - self.edad_inicial[indice]) / 100

    ataque = base_ataque * factor_salud * factor_hambre * factor_sed * factor_cansancio * factor_temperatura * factor_edad

    return max(0, min(100, ataque))
```

2. Valor de Defensa:

```python
def calcular_defensa(self, indice):
    base_defensa = self.genotipo_resistencia[indice] * 0.4 + self.genotipo_adaptabilidad[indice] * 0.3 + self.genotipo_supervivencia[indice] * 0.2

    factor_salud = self.salud[indice] / 100
    factor_hambre = max(0, 1 - self.hambre[indice] / 100)
    factor_sed = max(0, 1 - self.sed[indice] / 100)
    factor_cansancio = max(0, 1 - self.cansancio[indice] / 100)
    factor_temperatura = max(0, 1 - abs(self.temperatura_corporal[indice] - 37) / 10)
    factor_edad = 1 - (self.edad[indice] - self.edad_inicial[indice]) / 100

    defensa = base_defensa * factor_salud * factor_hambre * factor_sed * factor_cansancio * factor_temperatura * factor_edad

    return max(0, min(100, defensa))
```

Explicación del modelo:

1. Base de ataque/defensa: 
   - Para el ataque, se considera principalmente la fuerza, velocidad e inteligencia.
   - Para la defensa, se considera principalmente la resistencia, adaptabilidad y capacidad de supervivencia.

2. Factores de modificación:
   - Salud: A mayor salud, mejor rendimiento.
   - Hambre y Sed: Disminuyen el rendimiento a medida que aumentan.
   - Cansancio: Reduce el rendimiento a medida que aumenta.
   - Temperatura corporal: El rendimiento óptimo es a 37°C, y disminuye a medida que se aleja de este valor.
   - Edad: El rendimiento disminuye con el tiempo a medida que el humano envejece.

3. Cálculo final:
   - Se multiplica la base por todos los factores de modificación.
   - El resultado se limita entre 0 y 100 para mantenerlo en un rango manejable.

Este modelo proporciona un balance entre los diferentes factores que afectan el rendimiento de un humano en términos de ataque y defensa. Puedes ajustar los pesos y las fórmulas según las necesidades específicas de tu simulación.

Para usar estas funciones, podrías hacerlo así:

```python
ataque_humano_0 = self.calcular_ataque(0)
defensa_humano_0 = self.calcular_defensa(0)

print(f"Humano 0 - Ataque: {ataque_humano_0:.2f}, Defensa: {defensa_humano_0:.2f}")
```

Este modelo permite que los valores de ataque y defensa fluctúen dinámicamente basándose en el estado actual del humano, lo que puede añadir profundidad y realismo a tu simulación.

### 6. Dinosaurios

Entendido. Vamos a ajustar los valores para que sean más realistas en comparación con un humano cuyo poder de ataque máximo es 100. Esto significa que los dinosaurios más poderosos tendrán valores muy por encima de 100, reflejando su fuerza superior en comparación con los humanos.

Aquí está una versión revisada y más realista de los valores, considerando la escala humana:

```python
dinosaurios = {
    "braquiosaurio": {
        "ataque": 150,  # Principalmente por su tamaño y peso
        "defensa": 300  # Alta defensa debido a su enorme tamaño
    },
    "triceratops": {
        "ataque": 250,  # Cuernos y pico poderosos
        "defensa": 300  # Escudo óseo muy efectivo
    },
    "pteranodonte": {
        "ataque": 80,   # Garras y pico, pero no tan fuerte como otros
        "defensa": 60   # Estructura ósea ligera, vulnerable
    },
    "velociraptor": {
        "ataque": 180,  # Garras afiladas, velocidad e inteligencia
        "defensa": 100  # Tamaño relativamente pequeño
    },
    "tiranosaurio_rex": {
        "ataque": 400,  # Mandíbulas extremadamente poderosas
        "defensa": 350  # Tamaño y fuerza imponentes
    },
    "carnotauro": {
        "ataque": 300,  # Depredador poderoso
        "defensa": 250  # Buen tamaño y fuerza
    },
    "estegosaurio": {
        "ataque": 200,  # Cola con pinchos peligrosa
        "defensa": 280  # Placas dorsales y pinchos defensivos
    },
    "anquilosaurio": {
        "ataque": 220,  # Cola de maza potente
        "defensa": 400  # Armadura extremadamente resistente
    },
    "iguanodonte": {
        "ataque": 150,  # "Pulgares" afilados, pero principalmente herbívoro
        "defensa": 180  # Tamaño considerable y cierta capacidad defensiva
    }
}
```

Explicación de los cambios:

1. Braquiosaurio: Aumentado significativamente debido a su tamaño colosal.
2. Triceratops: Incrementado por su formidable capacidad ofensiva y defensiva.
3. Pteranodonte: Ligeramente reducido, ya que no era tan poderoso en comparación con los dinosaurios terrestres.
4. Velociraptor: Aumentado, pero no tanto como los más grandes, reflejando su tamaño real (más pequeño de lo que se muestra en películas).
5. Tiranosaurio Rex: Significativamente aumentado, representando su posición como uno de los depredadores más temibles.
6. Carnotauro: Incrementado para reflejar su naturaleza de depredador eficaz.
7. Estegosaurio: Aumentado, especialmente en defensa, por su armadura natural.
8. Anquilosaurio: Defensa muy aumentada debido a su armadura extremadamente efectiva.
9. Iguanodonte: Moderadamente aumentado, reconociendo su tamaño pero también su naturaleza menos agresiva.

Estos valores ahora reflejan mejor las capacidades reales de estos dinosaurios en relación con un humano. Por ejemplo, un T-Rex con un ataque de 400 sugiere que es cuatro veces más poderoso que el ataque máximo de un humano, lo cual es una representación más realista de su fuerza comparativa.

Para usar estos valores en tu simulación, podrías compararlos directamente con los valores de los humanos. Por ejemplo:

```python
def comparar_fuerza(humano_ataque, dino_nombre):
    dino_ataque = dinosaurios[dino_nombre]["ataque"]
    ratio = dino_ataque / humano_ataque
    print(f"El {dino_nombre} es {ratio:.2f} veces más fuerte que el humano en ataque.")

# Ejemplo de uso
ataque_humano = calcular_ataque(0)  # Suponiendo que esto devuelve el ataque del humano 0
comparar_fuerza(ataque_humano, "tiranosaurio_rex")
```

Este enfoque te permitirá tener una comparación más realista entre humanos y dinosaurios en tu simulación.

### 7. **Implementación**

El modelo requiere implementar estas probabilidades en un simulador que avance en unidades discretas de tiempo, evaluando el estado de cada agente y seleccionando acciones en función de las necesidades y condiciones del entorno. La simulación también deberá gestionar el cambio de clima, la reproducción y muerte de entidades, y la interacción entre diferentes tipos de agentes.

Este modelo matemático y probabilístico proporciona una estructura robusta para simular un ecosistema complejo, permitiendo ajustes finos en función de los objetivos del estudio y las características deseadas del simulador.
