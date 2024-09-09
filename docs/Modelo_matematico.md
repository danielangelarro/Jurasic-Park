# Documentación de Modelos Matemáticos

Esta documentación explica detalladamente los modelos matemáticos utilizados en la simulación.

## Modelos utilizados en ***app/models/comunidad.py***

### 1. **Genotipos**
Cada humano está modelado con diferentes características genéticas, que afectan su comportamiento y capacidad de supervivencia. Estos genotipos son:

- **Fuerza**: Distribución normal con media 50 y desviación estándar 10. Se utiliza para calcular la capacidad de ataque.
- **Velocidad**: Distribución normal con media 50 y desviación estándar 10. Afecta el desplazamiento y contribuye al cálculo del ataque.
- **Resistencia**: Distribución normal con media 50 y desviación estándar 10. Afecta el cansancio, la capacidad de defenderse y la resistencia al hambre y la sed.
- **Inteligencia**: Distribución normal con media 50 y desviación estándar 10. Mejora la capacidad de tomar decisiones y aumenta la resistencia.
- **Adaptabilidad**: Distribución normal con media 50 y desviación estándar 10. Afecta la capacidad de adaptarse a nuevas condiciones y terrenos.
- **Supervivencia**: Distribución normal con media 50 y desviación estándar 10. Aumenta la capacidad de sobrevivir en situaciones críticas.

#### **Interacciones Genotípicas**
Las interacciones entre los diferentes genotipos son modeladas para reflejar la naturaleza compensatoria de algunas características:
- **Alta inteligencia** reduce la fuerza (`0.9x`).
- **Alta resistencia** reduce la fuerza (`0.85x`).
- **Alta fuerza** reduce la velocidad (`0.85x`).
- **Alta velocidad** reduce la resistencia (`0.9x`).
- **Alta inteligencia** aumenta la resistencia (`1.1x`).
- **Alta fuerza y resistencia** reducen la inteligencia (`0.85x`).

### 2. **Cálculo de Ataque**
El modelo de ataque se calcula en función de varios factores:
- **Base de ataque**: Una combinación ponderada de fuerza (40%), velocidad (30%) e inteligencia (20%).
  
  \[
  $\text{Base de ataque} = 0.4 \times \text{Fuerza} + 0.3 \times \text{Velocidad} + 0.2 \times \text{Inteligencia}$
  \]

- **Penalización por baja resistencia**: Si la resistencia es menor a 30, se aplica una penalización del 20%.
  
  \[
  $\text{Base de ataque} \times 0.8$
  \]

- Factores adicionales que modifican el ataque:
  - **Salud**: Factor proporcional al porcentaje de salud.
  - **Hambre**: Penalización en función del nivel de hambre (mayor hambre, menor ataque).
  - **Sed**: Penalización en función del nivel de sed.
  - **Cansancio**: Penalización en función del cansancio.
  - **Temperatura corporal**: Penalización si la temperatura se aleja de 37°C.
  - **Edad**: Penalización basada en la diferencia entre la edad actual y la edad inicial.

El ataque final se obtiene multiplicando la base de ataque por todos los factores:

\[
$\text{Ataque} = \text{Base de ataque} \times \text{Factor salud} \times \text{Factor hambre} \times \text{Factor sed} \times \text{Factor cansancio} \times \text{Factor temperatura} \times \text{Factor edad}$
\]

### 3. **Cálculo de Defensa**
La defensa de cada humano se calcula de manera similar al ataque, utilizando diferentes genotipos:
- **Base de defensa**: Combinación ponderada de resistencia (40%), adaptabilidad (30%) y supervivencia (20%).

  \[
  $\text{Base de defensa} = 0.4 \times \text{Resistencia} + 0.3 \times \text{Adaptabilidad} + 0.2 \times \text{Supervivencia}$
  \]

- Los factores adicionales que modifican la defensa son idénticos a los del ataque: salud, hambre, sed, cansancio, temperatura corporal y edad.

El cálculo final es:

\[
$\text{Defensa} = \text{Base de defensa} \times \text{Factor salud} \times \text{Factor hambre} \times \text{Factor sed} \times \text{Factor cansancio} \times \text{Factor temperatura} \times \text{Factor edad}$
\]

### 4. **Actualización de Estados Fisiológicos**
Los humanos experimentan cambios fisiológicos en cada ciclo de la simulación:
- **Hambre**: Aumenta de acuerdo a una función logarítmica del tiempo, con una tasa de incremento de 0.1.
  
  \[
  $\text{Hambre} = \min(0.1 \times \log(t + 1) + \text{Hambre anterior}, 100)$
  \]

- **Sed**: Aumenta con una tasa logarítmica de 0.2.
  
  \[
  $\text{Sed} = \min(0.2 \times \log(t + 1) + \text{Sed anterior}, 100)$
  \]

- **Cansancio**: Aumenta en función de la resistencia genética y el tiempo.
  
  \[
  $\text{Cansancio} = \min(0.15 \times \log(t + 1) \times \left(1 - \frac{\text{Resistencia}}{100}\right) + \text{Cansancio anterior}, 100)$
  \]

Si la resistencia genética de un humano es alta, se aplica un factor de mejora en el hambre, la sed y el cansancio.

### 5. **Interacciones con Dinosaurios**
Los humanos interactúan con dinosaurios en función de su ataque y defensa:
- **Ataque y defensa de humanos**: Se calculan por humano y se suman para cada posición en el mapa donde se encuentren varios humanos.
- **Comparación con dinosaurios**: Si el ataque del dinosaurio en una posición es mayor que la defensa total de los humanos, los humanos mueren.

### 6. **Acciones de Supervivencia**
#### **Buscar Agua**
- Los humanos seleccionan la acción de buscar agua en función de su nivel de sed.
- La probabilidad de éxito se calcula como una combinación de factores del terreno y la adaptabilidad.

#### **Cazar**
- La acción de cazar sigue un proceso similar al de buscar agua, con probabilidades que dependen del terreno.

#### **Desplazamiento**
- Los humanos se desplazan en función de su velocidad genética. Se genera un movimiento aleatorio modificado por un factor de velocidad y se limita al tamaño del entorno.

### 7. **Reproducción**
El proceso de reproducción considera varios factores:
- **Probabilidad de selección**: Basada en la salud, la edad (más alta entre 18 y 35 años), y el tiempo desde la última reproducción.
  
  \[
  $P(\text{reproducción}) = 0.1 + \frac{\text{Salud}}{100} + \text{EdadMod} + \text{ParejaMod}$
  \]

- **Probabilidad de éxito**: Depende de la supervivencia genética.

### 8. **Probabilidades**
- **Probabilidad de selección**: Proporcional al estado fisiológico.

  \[
  $P(\text{selección}) = \frac{\text{estado}}{100}$
  \]

- **Probabilidad de éxito**: Una combinación de un valor base (0.5 o 0.3 según el contexto) más un modificador que depende del terreno o la genética.

  \[
  $P(\text{éxito}) = \text{base} + \text{modificador}$
  \]

## Modelos utilizados en ***app/models/entorno.py***

### 1. **Matriz de transición de clima (MATRIZ_CLIMA)**
   - La **Matriz de transición de clima** define las probabilidades de que el clima cambie de un estado a otro en cada iteración del simulador.
   - Es un **modelo de Markov**: las probabilidades de transición dependen solo del clima actual, no del clima en estados anteriores.
   
   ```python
   MATRIZ_CLIMA = np.array([
       [0.7, 0.2, 0.1],  # Soleado
       [0.3, 0.4, 0.3],  # Tormenta
       [0.4, 0.3, 0.3]   # Lluvioso
   ])
   ```
   - Cada fila de la matriz corresponde al estado actual del clima, y las columnas representan las probabilidades de cambiar a otro estado.
     - Si el clima es **soleado** (primera fila), tiene un 70% de probabilidad de permanecer soleado, un 20% de cambiar a tormenta, y un 10% de volverse lluvioso.
     - Si el clima es **tormenta** (segunda fila), tiene un 40% de quedarse en tormenta, 30% de volverse soleado y 30% de volverse lluvioso.

### 2. **Probabilidad de buscar agua (probabilidad_buscar_agua)**

   Este método calcula la probabilidad de que los dinosaurios busquen agua, basada en dos factores:
   - **Tipo de terreno:** El terreno en el que se encuentra el dinosaurio influye en la necesidad de buscar agua.
   - **Clima:** El clima afecta la probabilidad general de que se busque agua.

   El modelo combina ambas probabilidades multiplicándolas:
   ```python
   probabilidad = probabilidad_terreno[tipo_terreno] * probabilidad_clima[self.clima]
   ```

   - **Modelo de probabilidad basada en el terreno:**
     - Ejemplo: En el desierto, la probabilidad de buscar agua es alta (0.9), mientras que en el agua es baja (0.1).
   - **Modelo de probabilidad basada en el clima:**
     - Ejemplo: En un clima soleado, la probabilidad de buscar agua es alta (0.8), mientras que en clima lluvioso es baja (0.1).
   - La probabilidad final es el producto de ambas probabilidades. Si el terreno es **desierto** y el clima es **soleado**, la probabilidad final será \( 0.9 \times 0.8 = 0.72 \), lo que significa que hay un 72% de que el dinosaurio busque agua.

### 3. **Probabilidad de cazar (probabilidad_cazar)**
   Este método calcula la probabilidad de que un dinosaurio intente cazar, y sigue la misma estructura que el cálculo de la probabilidad de buscar agua:
   
   - **Probabilidad basada en el terreno:** Similar a buscar agua, el tipo de terreno influye en la probabilidad de cazar. En el desierto (0.8), la probabilidad es mayor que en la pradera (0.2).
   - **Probabilidad basada en el clima:** Un clima soleado tiene mayor probabilidad (0.7) de promover la caza, mientras que un clima lluvioso la disminuye (0.2).
   
   La probabilidad final también se calcula multiplicando ambas:
   ```python
   probabilidad_final = probabilidad_terreno[tipo_terreno] * probabilidad_clima[self.clima]
   ```
   Por ejemplo, si el terreno es **sabana** y el clima es **soleado**, la probabilidad de cazar será \( 0.5 \times 0.7 = 0.35 \), es decir, un 35% de que el dinosaurio intente cazar.

### 4. **Generación de dinosaurios (generate_dinosaurios)**
   - En este modelo, se genera una colección de dinosaurios en el terreno, considerando la relación entre el tipo de terreno y el clima.
   - Para cada posición en el terreno, se filtran los dinosaurios que pueden habitar el tipo de terreno en esa posición (usando la función `filter`).
   - Luego, se ordenan según su **probabilidad de aparición**, que probablemente sea una función que dependa del clima y el terreno.
   - Dependiendo de si el dinosaurio es solitario o no, se genera una cantidad aleatoria de ellos (entre 1 o 4) usando `np.random.randint`.
   - Finalmente, la fuerza de ataque de los dinosaurios en esa posición se acumula multiplicando el número de dinosaurios por su atributo de ataque.

### Modelos implícitos:
   - **Modelo de probabilidad discreta (Random Choice):** En la función `cambiar_clima`, se selecciona el próximo estado del clima utilizando una distribución de probabilidad discreta dada por la matriz de transición, que es una aplicación del **modelo de cadenas de Markov**.
   - **Probabilidad combinada:** Tanto en la búsqueda de agua como en la caza, se utiliza la combinación de probabilidades de diferentes factores (terreno y clima) multiplicando los valores asociados.

Estos modelos permiten simular un ecosistema dinámico y realista, donde tanto los dinosaurios como el entorno (clima, terreno) interactúan entre sí para influir en el comportamiento de los agentes (dinosaurios).
