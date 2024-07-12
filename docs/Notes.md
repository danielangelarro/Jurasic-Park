# Notes
===

Aquí tienes una lista aproximada de la edad máxima, tiempo de gestación y edad de adultez para los dinosaurios mencionados. Ten en cuenta que estos datos son estimaciones basadas en la información paleontológica disponible y pueden variar según diferentes estudios:

1. BRAQUIOSAURIO:
   - Edad máxima: 100 años
   - Tiempo de gestación: 1 año
   - Edad de adultez: 20 años

2. Triceratops:
   - Edad máxima: 70 años
   - Tiempo de gestación: 6 meses
   - Edad de adultez: 16 años

3. Pteranodonte:
   - Edad máxima: 40 años
   - Tiempo de gestación: 2-3 meses
   - Edad de adultez: 7 años

4. Velociraptor:
   - Edad máxima: 25 años
   - Tiempo de gestación: 3-4 meses
   - Edad de adultez: 2 años

5. Tiranosaurio-rex:
   - Edad máxima: 30 años
   - Tiempo de gestación: 6 meses
   - Edad de adultez: 20 años

6. Carnotauro:
   - Edad máxima: 40 años
   - Tiempo de gestación: 5 meses
   - Edad de adultez: 15 años

7. Estegosaurio:
   - Edad máxima: 75 años
   - Tiempo de gestación: 7 meses
   - Edad de adultez: 18 años

8. Anquilosaurio:
   - Edad máxima: 70 años
   - Tiempo de gestación: 6 meses
   - Edad de adultez: 17 años

9. Iguanodonte:
   - Edad máxima: 60 años
   - Tiempo de gestación: 5 meses
   - Edad de adultez: 14 años

Es importante señalar que estos datos son aproximaciones basadas en evidencia fósil limitada y comparaciones con reptiles modernos. La precisión de estas estimaciones puede variar, y nuevos descubrimientos podrían modificar estos números en el futuro.

### Creación de la Entidad Humano

Definimos una clase `Humano` con diversas características y un conjunto de acciones que puede realizar dependiendo de la zona y la situación en la que se encuentra.

```python
import random

class Humano:
    def __init__(self, nombre, edad, sexo, hambre, sed, cansancio, habilidades):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.hambre = hambre
        self.sed = sed
        self.cansancio = cansancio
        self.habilidades = habilidades
        self.posicion = (0, 0)
    
    def set_posicion(self, x, y):
        self.posicion = (x, y)
    
    def acciones(self, zona, situacion):
        acciones_disponibles = []
        
        if zona == "Sabana":
            acciones_disponibles.extend(["buscar_agua", "cazar", "recolectar", "descansar"])
        elif zona == "Desierto":
            acciones_disponibles.extend(["buscar_sombra", "buscar_agua", "descansar"])
        elif zona == "Acantilado":
            acciones_disponibles.extend(["escalar", "explorar"])
        elif zona == "Pantano":
            acciones_disponibles.extend(["pescar", "buscar_comida", "evitar_peligros"])
        elif zona == "Agua":
            acciones_disponibles.extend(["nadar", "pescar"])
        
        if situacion == "hambre":
            acciones_disponibles.append("buscar_comida")
        if situacion == "sed":
            acciones_disponibles.append("buscar_agua")
        if situacion == "cansancio":
            acciones_disponibles.append("descansar")
        
        return acciones_disponibles

# Ejemplo de uso
humano = Humano(nombre="John", edad=25, sexo="Macho", hambre=50, sed=40, cansancio=30, habilidades={"caza": 70, "recoleccion": 50})
humano.set_posicion(5, 5)
acciones = humano.acciones(zona="Sabana", situacion="hambre")
print(acciones)
```

### Lista de Acciones

Dependiendo de la zona y la situación, un humano puede realizar las siguientes acciones:

1. **Sabana**:
   - Buscar agua
   - Cazar
   - Recolectar
   - Descansar

2. **Desierto**:
   - Buscar sombra
   - Buscar agua
   - Descansar

3. **Acantilado**:
   - Escalar
   - Explorar

4. **Pantano**:
   - Pescar
   - Buscar comida
   - Evitar peligros

5. **Agua**:
   - Nadar
   - Pescar

### Simulación con Algoritmo Genético

Para realizar una simulación con un algoritmo genético, consideramos las siguientes características de los humanos:

1. **Características Genéticas**:
   - Fuerza
   - Velocidad
   - Resistencia
   - Inteligencia
   - Adaptabilidad

2. **Habilidades**:
   - Caza
   - Recolección
   - Pesca
   - Exploración

3. **Estados Fisiológicos**:
   - Nivel de hambre
   - Nivel de sed
   - Nivel de cansancio

#### Mutación

Las mutaciones pueden introducir cambios en los atributos genéticos y habilidades. Ejemplos de mutaciones incluyen:

- Incremento o decremento en la fuerza, velocidad, resistencia, inteligencia, y adaptabilidad.
- Mejoras o empeoramientos en las habilidades de caza, recolección, pesca y exploración.
- Cambios en la tolerancia al hambre, sed y cansancio.

```python
def mutacion(humano):
    if random.random() < 0.1:  # 10% de probabilidad de mutación
        atributo_a_mutar = random.choice(['fuerza', 'velocidad', 'resistencia', 'inteligencia', 'adaptabilidad'])
        cambio = random.uniform(-10, 10)
        setattr(humano, atributo_a_mutar, getattr(humano, atributo_a_mutar) + cambio)
    
    if random.random() < 0.1:  # 10% de probabilidad de mutación
        habilidad_a_mutar = random.choice(['caza', 'recoleccion', 'pesca', 'exploracion'])
        cambio = random.uniform(-10, 10)
        humano.habilidades[habilidad_a_mutar] += cambio

# Ejemplo de mutación
mutacion(humano)
```

#### Cruzamiento

El cruzamiento combina las características de dos individuos para crear una nueva generación. 

```python
def cruzamiento(padre, madre):
    hijo = Humano(
        nombre="Hijo",
        edad=0,
        sexo=random.choice(["Macho", "Hembra"]),
        hambre=50,
        sed=50,
        cansancio=50,
        habilidades={}
    )
    
    # Promedio de los atributos de los padres
    for atributo in ['fuerza', 'velocidad', 'resistencia', 'inteligencia', 'adaptabilidad']:
        setattr(hijo, atributo, (getattr(padre, atributo) + getattr(madre, atributo)) / 2)
    
    # Promedio de las habilidades de los padres
    for habilidad in ['caza', 'recoleccion', 'pesca', 'exploracion']:
        hijo.habilidades[habilidad] = (padre.habilidades[habilidad] + madre.habilidades[habilidad]) / 2
    
    return hijo

# Ejemplo de cruzamiento
madre = Humano(nombre="Jane", edad=22, sexo="Hembra", hambre=50, sed=40, cansancio=30, habilidades={"caza": 60, "recoleccion": 60})
hijo = cruzamiento(humano, madre)
print(vars(hijo))
```

### Resumen

- La clase `Humano` incluye características fisiológicas, habilidades y posición.
- Las acciones dependen de la zona y situación en la que se encuentra el humano.
- Para la simulación con un algoritmo genético, se consideran características genéticas, habilidades y estados fisiológicos.
- Se implementan funciones de mutación y cruzamiento para simular la evolución de las características a través de generaciones.

### Resumen de Influencia de Características Genéticas y Habilidades en la Ejecución de Acciones

#### Acciones y su Relación con Características Genéticas y Habilidades

1. **Buscar agua**
   - **Estado fisiológico:** Reduce el nivel de sed.
   - **Habilidad:** Ninguna específica.
   - **Genética:** Adaptabilidad puede influir en la eficiencia para encontrar agua en diferentes ambientes.

2. **Cazar**
   - **Estado fisiológico:** Reduce el nivel de hambre si tiene éxito.
   - **Habilidad:** 
     - **Caza**: Influye directamente en la probabilidad de éxito.
   - **Genética:** 
     - **Fuerza**: Aumenta la probabilidad de éxito.
     - **Velocidad**: Puede aumentar la probabilidad de éxito.

3. **Recolectar**
   - **Estado fisiológico:** Reduce el nivel de hambre si tiene éxito.
   - **Habilidad:** 
     - **Recolección**: Influye directamente en la probabilidad de éxito.
   - **Genética:** 
     - **Inteligencia**: Puede aumentar la eficiencia y éxito en la recolección.

4. **Descansar**
   - **Estado fisiológico:** Reduce el nivel de cansancio.
   - **Habilidad:** Ninguna específica.
   - **Genética:** 
     - **Resistencia**: Puede influir en la rapidez y eficiencia del descanso.

5. **Buscar sombra**
   - **Estado fisiológico:** Reduce el nivel de cansancio y sed.
   - **Habilidad:** Ninguna específica.
   - **Genética:** 
     - **Adaptabilidad**: Puede influir en la eficiencia para encontrar sombra en diferentes ambientes.

6. **Escalar**
   - **Estado fisiológico:** No tiene un efecto directo.
   - **Habilidad:** 
     - **Exploración**: Influye en la probabilidad de éxito al escalar.
   - **Genética:** 
     - **Fuerza**: Aumenta la probabilidad de éxito.
     - **Resistencia**: Aumenta la probabilidad de éxito.

7. **Explorar**
   - **Estado fisiológico:** No tiene un efecto directo.
   - **Habilidad:** 
     - **Exploración**: Influye en la probabilidad de éxito al explorar.
   - **Genética:** 
     - **Inteligencia**: Puede aumentar la eficiencia y éxito en la exploración.
     - **Adaptabilidad**: Puede influir en la capacidad de adaptarse a nuevos ambientes.

8. **Pescar**
   - **Estado fisiológico:** Reduce el nivel de hambre si tiene éxito.
   - **Habilidad:** 
     - **Pesca**: Influye directamente en la probabilidad de éxito.
   - **Genética:** 
     - **Paciencia**: (si se considera como un factor de inteligencia o resistencia).

9. **Nadar**
   - **Estado fisiológico:** No tiene un efecto directo.
   - **Habilidad:** Ninguna específica.
   - **Genética:** 
     - **Resistencia**: Puede influir en la eficiencia y habilidad para nadar.

10. **Evitar peligros**
    - **Estado fisiológico:** Mantiene el nivel de vida.
    - **Habilidad:** 
      - **Exploración**: Influye en la capacidad de evitar peligros.
    - **Genética:** 
      - **Velocidad**: Puede influir en la capacidad de escapar de peligros.
      - **Inteligencia**: Puede influir en la capacidad de reconocer y evitar peligros.

### Ejemplo de Implementación en el Código

```python
def ejecutar_accion(self, accion):
    if accion == "buscar_agua":
        self.sed -= 10
        print(f"{self.nombre} ha buscado agua y ahora tiene {self.sed} de sed.")
    elif accion == "cazar":
        exito = random.random() < (self.habilidades["caza"] + self.genetica["fuerza"] + self.genetica["velocidad"]) / 300
        if exito:
            self.hambre -= 20
            print(f"{self.nombre} ha cazado con éxito y ahora tiene {self.hambre} de hambre.")
        else:
            print(f"{self.nombre} ha fallado en la caza.")
    elif accion == "recolectar":
        exito = random.random() < (self.habilidades["recoleccion"] + self.genetica["inteligencia"]) / 200
        if exito:
            self.hambre -= 10
            print(f"{self.nombre} ha recolectado alimentos y ahora tiene {self.hambre} de hambre.")
        else:
            print(f"{self.nombre} ha fallado en la recolección.")
    elif accion == "descansar":
        self.cansancio -= 15 * (1 + self.genetica["resistencia"] / 100)
        print(f"{self.nombre} ha descansado y ahora tiene {self.cansancio} de cansancio.")
    # Añadir más acciones según sea necesario.

# Ejemplo de uso
genetica = {
    "fuerza": 70,
    "velocidad": 50,
    "resistencia": 60,
    "inteligencia": 80,
    "adaptabilidad": 65
}

habilidades = {
    "caza": 70,
    "recoleccion": 50,
    "pesca": 60,
    "exploracion": 55
}

humano = Humano(
    nombre="John",
    edad=25,
    sexo="Macho",
    hambre=50,
    sed=40,
    cansancio=30,
    habilidades=habilidades,
    genetica=genetica
)
humano.set_posicion(5, 5)
acciones = humano.acciones(zona="Sabana", situacion="hambre")
print(f"Acciones disponibles: {acciones}")

# Ejecutar una acción
humano.ejecutar_accion("cazar")
```

### Resumen de la Influencia

- **Buscar agua:** Influencia de la adaptabilidad genética.
- **Cazar:** Influencia de las habilidades de caza y las características genéticas de fuerza y velocidad.
- **Recolectar:** Influencia de las habilidades de recolección y la inteligencia genética.
- **Descansar:** Influencia de la resistencia genética.
- **Buscar sombra:** Influencia de la adaptabilidad genética.
- **Escalar:** Influencia de las habilidades de exploración y las características genéticas de fuerza y resistencia.
- **Explorar:** Influencia de las habilidades de exploración y las características genéticas de inteligencia y adaptabilidad.
- **Pescar:** Influencia de las habilidades de pesca y la paciencia genética.
- **Nadar:** Influencia de la resistencia genética.
- **Evitar peligros:** Influencia de las habilidades de exploración y las características genéticas de velocidad e inteligencia.

Este resumen y la implementación refactorizada ayudan a ilustrar cómo las diferentes características genéticas y habilidades influyen en la ejecución de las acciones dentro del ecosistema.

Para utilizar una LLM (Large Language Model) para generar árboles de decisiones y características de cada humano en dependencia de su personalidad, puedes seguir los siguientes pasos:

1. **Definir Personalidades y Características:**
   Define un conjunto de personalidades y sus características asociadas. Cada personalidad puede tener un conjunto de habilidades y estados fisiológicos específicos.

2. **Generar Árboles de Decisiones:**
   Usa la LLM para generar árboles de decisiones que se adapten a las personalidades definidas. Estos árboles de decisiones pueden determinar las acciones preferidas de cada humano según su personalidad.

3. **Entrenamiento y Ajuste:**
   Si tienes datos históricos o simulaciones anteriores, puedes usarlos para entrenar y ajustar los modelos generados por la LLM para mejorar su precisión y relevancia.

4. **Implementación en el Código:**
   Integra la generación dinámica de características y árboles de decisiones en tu simulador, permitiendo que cada humano tenga una personalidad única y reaccione de acuerdo a su perfil.

### Paso 1: Definir Personalidades y Características

Define algunas personalidades y sus características. Por ejemplo:

```python
personalidades = {
    "Explorador": {
        "habilidades": {"exploracion": 80, "caza": 50, "recoleccion": 60, "pesca": 40},
        "genetica": {"fuerza": 60, "velocidad": 70, "resistencia": 80, "inteligencia": 70, "adaptabilidad": 90}
    },
    "Cazador": {
        "habilidades": {"exploracion": 50, "caza": 90, "recoleccion": 40, "pesca": 50},
        "genetica": {"fuerza": 90, "velocidad": 80, "resistencia": 70, "inteligencia": 60, "adaptabilidad": 50}
    },
    "Recolector": {
        "habilidades": {"exploracion": 60, "caza": 40, "recoleccion": 90, "pesca": 50},
        "genetica": {"fuerza": 50, "velocidad": 60, "resistencia": 70, "inteligencia": 90, "adaptabilidad": 70}
    }
}
```

### Paso 2: Generar Árboles de Decisiones

Usa una LLM para generar árboles de decisiones basados en las personalidades. Aquí hay un ejemplo simplificado usando prompts para una LLM:

```python
import openai

def generar_arbol_decisiones(personalidad):
    prompt = f"Genera un árbol de decisiones para un humano con personalidad '{personalidad}'."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Ejemplo de uso
for personalidad in personalidades:
    arbol_decisiones = generar_arbol_decisiones(personalidad)
    print(f"Árbol de decisiones para {personalidad}:\n{arbol_decisiones}\n")
```

### Paso 3: Entrenamiento y Ajuste

Si tienes datos históricos, puedes usarlos para ajustar los árboles de decisiones generados. Esto puede ser hecho utilizando técnicas de aprendizaje automático para mejorar la precisión de las decisiones.

### Paso 4: Implementación en el Código

Integra la generación dinámica en tu simulador. Aquí hay un ejemplo de cómo hacerlo:

```python
class Humano:
    def __init__(self, nombre, edad, sexo, personalidad):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.personalidad = personalidad
        self.habilidades = personalidades[personalidad]["habilidades"]
        self.genetica = personalidades[personalidad]["genetica"]
        self.hambre = 50
        self.sed = 50
        self.cansancio = 50
        self.arbol_decisiones = generar_arbol_decisiones(personalidad)

    def ejecutar_accion(self, accion):
        # Implementar lógica de ejecución de acciones
        pass

# Ejemplo de uso
humano = Humano(nombre="John", edad=25, sexo="Macho", personalidad="Explorador")
print(f"Árbol de decisiones de {humano.nombre}: {humano.arbol_decisiones}")
```

### Integración de LLM para la Personalización

Para una integración completa, podrías desarrollar un flujo en el que se utilicen los modelos generados por la LLM para definir y ajustar continuamente las personalidades y los árboles de decisiones de los humanos en la simulación. Esto puede incluir ajustes dinámicos basados en las condiciones del ecosistema y las interacciones entre los humanos y los animales en el simulador.

### Prompt de llamada a la API LLM

```chatinput
Eres un experto en simulaciones y comportamiento humano. Quiero que generes un árbol de decisiones para un humano en un entorno natural. El árbol de decisiones debe depender del tipo de personalidad del humano y de las acciones que puede realizar en diferentes situaciones.

### Tipos de Personalidad:
1. Explorador: Prefiere descubrir nuevas áreas y tomar riesgos.
2. Cazador: Se enfoca en cazar animales y buscar alimento.
3. Recolector: Se especializa en recolectar recursos y alimentos del entorno.
4. Socializador: Prefiere interactuar con otros humanos y formar alianzas.
5. Constructor: Se enfoca en construir refugios y mejorar el entorno.

### Acciones Disponibles:
- Explorar
- Cazar
- Recolectar
- Pescar
- Descansar
- Socializar
- Construir
- Defenderse
- Buscar refugio
- Buscar agua
- Buscar comida

### Contexto General:
El humano se encuentra en un entorno natural con diferentes tipos de terrenos como bosques, desiertos, pantanos, sabanas y montañas. El humano puede experimentar diferentes necesidades como hambre, sed, cansancio, y puede enfrentar diferentes desafíos como la presencia de depredadores, condiciones climáticas adversas, y la necesidad de encontrar recursos y refugio.

### Instrucciones:
Genera un árbol de decisiones detallado para cada tipo de personalidad, considerando las acciones disponibles y el contexto general. El árbol de decisiones debe priorizar las acciones basadas en la personalidad del humano y su situación actual. Asegúrate de incluir las posibles ramificaciones y condiciones para cada decisión.

### Ejemplo:
- Personalidad: Explorador
  - Situación: El humano tiene hambre y sed, y hay depredadores cerca.
  - Árbol de decisiones:
    1. Evaluar el entorno inmediato para identificar fuentes de agua y alimentos seguros.
      - Si encuentra agua, ir a buscar agua.
      - Si encuentra comida, ir a recolectar/comer.
    2. Si no encuentra recursos inmediatos, decidir si es seguro explorar más lejos.
      - Si es seguro, explorar áreas cercanas.
      - Si no es seguro, buscar refugio.
    3. Priorizar la seguridad y evitar depredadores.
      - Si hay depredadores, buscar refugio primero.
      - Si no hay depredadores, proceder con la búsqueda de recursos.

Genera árboles de decisiones similares para los otros tipos de personalidad (Cazador, Recolector, Socializador, Constructor).
```

### Notas Finales

- **Tamaño del Prompt:** Los prompts más largos pueden dar más contexto a la LLM y mejorar la calidad de las respuestas.
- **Ajustes del Modelo:** Ajustar los parámetros del modelo como el `max_tokens` y `temperature` puede mejorar la relevancia de las respuestas.
- **Validación:** Es importante validar las decisiones generadas para asegurarse de que sean coherentes y útiles para la simulación. 

Implementar esta integración permite personalizar profundamente las decisiones y comportamientos de cada humano en tu simulador, mejorando la calidad y realismo de la simulación.

## Idea 2 para prompt

```chatinput
Genera un árbol de decisión en formato JSON para un humano con la siguiente personalidad: [PERSONALIDAD]. Las acciones disponibles son: 
cazar, recolectar, pescar, descansar, construir, buscar_refugio, huir, comunicar, aparearse_humano,
acercarse, gritar, moverse_humano, beber, atacar_humano. El árbol de decisión debe considerar las características genéticas 
(genetica.Fuerza, genetica.Velocidad, genetica.Resistencia, genetica.Inteligencia, genetica.Adaptabilidad), las habilidades 
(habilidades.Caza, habilidades.Recoleccion, habilidades.Pesca, habilidades.Exploracion) y los estados 
fisiológicos (is_alive, is_hambriento, is_sediento, cansancio) del humano. Las zonas son (sabana, desierto, pantano, praderaa, agua, acantilado). 
Define alternativas en caso de que la tarea no pueda cumplirse de tal manera que se intenten realizar todas.
No coloques el campo para la decision si la condition es falsa y no generes condiciones anidadas. 
genera el arbol de decision para cada una de las zonas.
Genera solamente el JSON, no menciones palabras de más. Utiliza el sistema de condicionales de python. La prioridad numero 1 de todo humano
es sobrevivir.

## Example
{
    "acciones": [
      {
        "condition": "not is_alive",
        "true": "return"
      },
      {
        "condition": "is_hambriento and habilidades.Caza > 50",
        "true": "cazar"
      },
      {
        "condition": "is_hambriento and habilidades.Recoleccion > 40",
        "true": "recolectar"
      },
      {
        "condition": "cansancio > 70",
        "true": "descansar"
      },
      {
        "condition": "genetica.Inteligencia > 60 and habilidades.Exploracion > 50",
        "true": "construir"
      },
      {
        "condition": "genetica.Adaptabilidad < 30",
        "true": "buscar_refugio"
      },
      {
        "condition": "genetica.Velocidad > 70",
        "true": "huir"
      },
      {
        "condition": "genetica.Inteligencia > 50",
        "true": "comunicar"
      },
      {
        "condition": "genetica.Resistencia > 50",
        "true": "aparearse_humano"
      },
      {
        "condition": "genetica.Fuerza > 60",
        "true": "atacar_humano"
      },
      {
        "condition": "True",
        "true": "acercarse"
      }
    ]
}
```

## Lista de Hipótesis

1. **Hipótesis de Supervivencia y Hábitat:**
   - **Hipótesis 1:** Los humanos que habitan en zonas con más recursos naturales (agua y vegetación) tendrán una mayor tasa de supervivencia.
   - **Hipótesis 2:** Los humanos en áreas peligrosas, como acantilados y pantanos, tendrán una mayor tasa de mortalidad debido a los ataques de depredadores y accidentes ambientales.

2. **Hipótesis de Comportamiento Social:**
   - **Hipótesis 3:** Los humanos que forman grupos de cooperación tienen una mayor tasa de supervivencia en comparación con los que actúan individualmente.
   - **Hipótesis 4:** Los humanos que comunican y comparten información sobre recursos y peligros tendrán una mayor tasa de supervivencia.

3. **Hipótesis de Evolución Genética:**
   - **Hipótesis 5:** La aplicación del algoritmo genético después de cada ciclo de reproducción resulta en una adaptación más rápida a las condiciones del parque jurásico.
   - **Hipótesis 6:** La aplicación del algoritmo genético al final de una simulación completa y la selección de los mejores sobrevivientes para la siguiente generación produce individuos más fuertes y adaptados en comparación con la selección en cada ciclo de reproducción.

4. **Hipótesis de Reproducción y Cuidados:**
   - **Hipótesis 7:** Las mujeres que tienen períodos de gestación más largos y cuidados postnatales mejorados tendrán crías con mayor tasa de supervivencia.
   - **Hipótesis 8:** Los humanos que se aparean con individuos que tienen habilidades mejoradas (por ejemplo, caza, recolección) producirán crías con mayor tasa de supervivencia y habilidades heredadas mejoradas.

5. **Hipótesis de Interacción con Dinosaurios:**
   - **Hipótesis 9:** Los humanos que desarrollan habilidades de huida y refugio tendrán una mayor tasa de supervivencia frente a ataques de dinosaurios.
   - **Hipótesis 10:** Los humanos que se enfrentan a dinosaurios con habilidades mejoradas de ataque y defensa tendrán una mayor probabilidad de supervivencia.

### Variables a Medir

Para probar estas hipótesis, es necesario definir y medir varias variables en la simulación, incluyendo:

- Tasa de supervivencia (número de humanos sobrevivientes / total de humanos)
- Número de recursos naturales consumidos (agua, alimentos)
- Tasa de mortalidad en diferentes hábitats
- Tamaño de los grupos de cooperación
- Frecuencia y eficacia de la comunicación
- Habilidades heredadas (caza, recolección, pesca, defensa, etc.)
- Número de crías y su tasa de supervivencia
- Frecuencia y resultado de interacciones con dinosaurios (ataques, huidas)
- Adaptaciones genéticas observadas después de cada generación

### Implementación de Experimentos

Para cada hipótesis, se pueden diseñar experimentos específicos dentro de la simulación. Por ejemplo, para la **Hipótesis 1**, se podría crear diferentes escenarios con humanos en distintas zonas del parque y medir la tasa de supervivencia en cada zona. Para la **Hipótesis 5** y **Hipótesis 6**, se puede comparar los resultados de la simulación aplicando el algoritmo genético en diferentes momentos y medir la adaptabilidad y habilidades de las nuevas generaciones.

Estos experimentos ayudarán a validar las hipótesis y proporcionarán información valiosa sobre la dinámica de la comunidad humana en el parque jurásico.
