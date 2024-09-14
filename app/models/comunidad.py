import numpy as np
from collections import Counter


class Comunidad:
    def __init__(self, n_humanos=10, tamano_entorno=10):
        self.n_humanos = n_humanos
        self.tamano = tamano_entorno
        self.hambre = np.zeros(n_humanos)
        self.sed = np.zeros(n_humanos)
        self.cansancio = np.zeros(n_humanos)
        self.salud = np.ones(n_humanos) * 100
        self.temperatura_corporal = np.zeros(n_humanos)
        self.genotipo_fuerza = np.random.normal(loc=50, scale=30, size=n_humanos)
        self.genotipo_velocidad = np.random.normal(loc=50, scale=30, size=n_humanos)
        self.genotipo_resistencia = np.random.normal(loc=50, scale=30, size=n_humanos)
        self.genotipo_inteligencia = np.random.normal(loc=50, scale=30, size=n_humanos)
        self.genotipo_adaptabilidad = np.random.normal(loc=50, scale=30, size=n_humanos)
        self.genotipo_supervivencia = np.random.normal(loc=50, scale=30, size=n_humanos)
        self.edad = np.random.randint(18, 60, size=n_humanos)
        self.edad_inicial = self.edad.copy()
        self.genero = np.random.choice(['masculino', 'femenino'], size=n_humanos)
        self.ultima_reproduccion = np.full(n_humanos, -3)  # Iniciar todas como nunca se han reproducido
        self.posiciones = np.random.randint(0, tamano_entorno, (n_humanos, 2))  # Posicion aleatoria en el entorno

        self.aplicar_interacciones_genotipicas()

    def aplicar_interacciones_genotipicas(self):
        # Condiciones aplicadas a nivel de comunidad usando operaciones vectorizadas

        # Aumento de inteligencia disminuye la fuerza
        self.genotipo_fuerza[self.genotipo_inteligencia > 0.7] *= 0.9

        # Aumentar resistencia reduce la fuerza
        self.genotipo_fuerza[self.genotipo_resistencia > 0.7] *= 0.85

        # Aumentar fuerza reduce la velocidad
        self.genotipo_velocidad[self.genotipo_fuerza > 0.7] *= 0.85

        # Aumentar velocidad reduce la resistencia
        self.genotipo_resistencia[self.genotipo_velocidad > 0.7] *= 0.9

        # Aumentar inteligencia mejora la eficiencia y aumenta resistencia
        self.genotipo_resistencia[self.genotipo_inteligencia > 0.7] *= 1.1

        # Alta fuerza y resistencia reduce la inteligencia
        condicion_fuerza_resistencia = (self.genotipo_fuerza > 0.6) & (self.genotipo_resistencia > 0.6)
        self.genotipo_inteligencia[condicion_fuerza_resistencia] *= 0.85

    def calcular_ataque(self, indice):
        base_ataque = (self.genotipo_fuerza[indice] * 0.4 +
                       self.genotipo_velocidad[indice] * 0.3 +
                       self.genotipo_inteligencia[indice] * 0.2)

        # Penalización por resistencia baja
        if self.genotipo_resistencia[indice] < 30:
            base_ataque *= 0.8  # Penalización del 20%

        factor_salud = self.salud[indice] / 100
        factor_hambre = max(0, 1 - self.hambre[indice] / 100)
        factor_sed = max(0, 1 - self.sed[indice] / 100)
        factor_cansancio = max(0, 1 - self.cansancio[indice] / 100)
        factor_temperatura = max(0, 1 - abs(self.temperatura_corporal[indice] - 37) / 10)
        factor_edad = 1 - (self.edad[indice] - self.edad_inicial[indice]) / 100

        ataque = base_ataque * factor_salud * factor_hambre * factor_sed * factor_cansancio * factor_temperatura * factor_edad

        return max(0, min(100, ataque))

    def calcular_defensa(self, indice):
        base_defensa = self.genotipo_resistencia[indice] * 0.4 + self.genotipo_adaptabilidad[indice] * 0.3 + \
                       self.genotipo_supervivencia[indice] * 0.2

        factor_salud = self.salud[indice] / 100
        factor_hambre = max(0, 1 - self.hambre[indice] / 100)
        factor_sed = max(0, 1 - self.sed[indice] / 100)
        factor_cansancio = max(0, 1 - self.cansancio[indice] / 100)
        factor_temperatura = max(0, 1 - abs(self.temperatura_corporal[indice] - 37) / 10)
        factor_edad = 1 - (self.edad[indice] - self.edad_inicial[indice]) / 100

        defensa = base_defensa * factor_salud * factor_hambre * factor_sed * factor_cansancio * factor_temperatura * factor_edad

        return max(0, min(100, defensa))

    def actualizar_estados_fisiologicos(self):
        for i in range(self.n_humanos):
            tiempo = self.edad[i] - self.edad_inicial[i]
            self.hambre[i] = min(max(0.1 * np.log(tiempo + 1) + self.hambre[i], 0), 100)
            self.sed[i] = min(max(0.2 * np.log(tiempo + 1) + self.sed[i], 0), 100)
            self.cansancio[i] = min(
                max(0.15 * np.log(tiempo + 1) * (1 - self.genotipo_resistencia[i] / 100) + self.cansancio[i], 0), 100)
            self.edad[i] += 1

            if self.genotipo_resistencia[i] > 0.7:
                self.hambre[i] *= 0.8  # Mejora la resistencia al hambre
                self.sed[i] *= 0.85  # Mejora la resistencia a la sed
                self.cansancio[i] *= 0.75  # Mejora la resistencia al cansancio

    def interaccion_dinosaurio(self, dinoasurios_por_posicion):
        posiciones_tuplas = [tuple(coord) for coord in self.posiciones]
        conteo = Counter(posiciones_tuplas)
        diccionario_conteo = dict(conteo)
        muerte = np.full(self.n_humanos, False, dtype=bool)

        for i, coord in enumerate(self.posiciones):
            coord = tuple(coord)
            cant_humanos = diccionario_conteo[coord]
            ataque_humanos = self.calcular_ataque(i) * cant_humanos
            defensa_humanos = self.calcular_defensa(i) * cant_humanos

            if dinoasurios_por_posicion[coord]["ataque"] > defensa_humanos:
                muerte[i] = True
            elif ataque_humanos > dinoasurios_por_posicion[coord]["defensa"]:
                pass

        return self.remove_humano(muerte)

    def buscar_agua(self, entorno):
        seleccion = np.random.rand(self.n_humanos) < self.probabilidad_seleccion(self.sed)
        éxito = np.zeros(self.n_humanos, dtype=bool)

        for i in range(self.n_humanos):
            tipo_terreno = entorno.terreno[self.posiciones[i][0], self.posiciones[i][1]]
            terreno_mod = entorno.probabilidad_buscar_agua(tipo_terreno)
            adaptabilidad_prom = self.genotipo_adaptabilidad[i] / 100
            éxito[i] = np.random.rand() < self.probabilidad_éxito(0.5, terreno_mod + adaptabilidad_prom)

        resultado = seleccion & éxito
        self.sed[resultado] = 0
        return resultado

    def buscar_comida(self, entorno):
        seleccion = np.random.rand(self.n_humanos) < self.probabilidad_seleccion(self.hambre)
        éxito = np.zeros(self.n_humanos, dtype=bool)

        for i in range(self.n_humanos):
            tipo_terreno = entorno.terreno[self.posiciones[i][0], self.posiciones[i][1]]
            terreno_mod = entorno.probabilidad_buscar_comida(tipo_terreno)
            éxito[i] = np.random.rand() < self.probabilidad_éxito(0.5, terreno_mod)

        resultado = seleccion & éxito
        self.hambre[resultado] = 0
        return resultado

    def desplazarse(self):
        for i in range(self.n_humanos):
            factor_velocidad = self.genotipo_velocidad[i] / 100
            factor_cansancio = (100 - self.cansancio[i]) / 100 
            factor_final = factor_velocidad * factor_cansancio 

            movimiento = np.random.randint(-1, 2, size=2) * int(factor_final * 3)  # Multiplicador de velocidad

            nueva_posicion = self.posiciones[i] + movimiento
            nueva_posicion = np.clip(nueva_posicion, 0, self.tamano - 1)  # Limitar al tamano del entorno

            # Actualizar la posición
            self.posiciones[i] = nueva_posicion

        return self.posiciones

    def descansar(self):
        seleccion = np.random.rand(self.n_humanos) < self.cansancio / 100
        exito = np.random.rand(self.n_humanos) < 0.5
        self.cansancio[exito] = 0
        return exito

    def probabilidad_seleccion(self, estado):
        return estado / 100

    def probabilidad_éxito(self, base, mod):
        return base + mod

    def probabilidad_seleccion_reproducirse(self, salud, edad, ultima_reproduccion):
        base = 0.1
        salud_mod = salud / 100
        edad_mod = 1 if 18 <= edad <= 35 else 0.5  # Más probable entre 18-35 anos
        pareja_mod = 0.5 if ultima_reproduccion < -2 else 0  # Puede reproducirse si no ha tenido hijos en los últimos 2 ciclos
        return base + salud_mod + edad_mod + pareja_mod

    def reproducirse(self):
        nacimientos = 0
        hijos = []

        for i in range(self.n_humanos):
            if self.genero[i] == 'femenino' and 15 <= self.edad[i] <= 50:
                seleccion = np.random.rand() < self.probabilidad_seleccion_reproducirse(self.salud[i], self.edad[i],
                                                                                        self.ultima_reproduccion[i])
                éxito = np.random.rand() < self.probabilidad_éxito(0.3, self.genotipo_supervivencia[i])
                if seleccion and éxito:
                    hijos += self.crear_hijos()

        self.n_humanos += len(hijos)
        self.ultima_reproduccion[self.ultima_reproduccion >= 0] += 1

        if hijos:
            self.agregar_hijos(hijos)

        return len(hijos)

    def crear_hijos(self):
        indices_masculino = np.where(self.genero == "masculino")[0]
        indices_femenino = np.where(self.genero == "femenino")[0]
        num_hijos = np.random.randint(1, 4)
        hijos = []

        if len(indices_masculino) == 0 or len(indices_femenino) == 0:
            return []

        for _ in range(num_hijos):
            padre = np.random.choice(indices_masculino)
            madre = np.random.choice(indices_femenino)
            hijo = self.ferilizar(padre, madre)
            hijos.append(hijo)
        return hijos

    def ferilizar(self, padre, madre):
        genotipo_fuerza = self.genotipo_fuerza[padre] if np.random.rand() > 0.5 else self.genotipo_fuerza[madre]
        genotipo_velocidad = self.genotipo_velocidad[padre] if np.random.rand() > 0.5 else self.genotipo_velocidad[madre]
        genotipo_resistencia = self.genotipo_resistencia[padre] if np.random.rand() > 0.5 else self.genotipo_resistencia[madre]
        genotipo_inteligencia = self.genotipo_inteligencia[padre] if np.random.rand() > 0.5 else self.genotipo_inteligencia[madre]
        genotipo_adaptabilidad = self.genotipo_adaptabilidad[padre] if np.random.rand() > 0.5 else self.genotipo_adaptabilidad[madre]
        genotipo_supervivencia = self.genotipo_supervivencia[padre] if np.random.rand() > 0.5 else self.genotipo_supervivencia[madre]

        genotipo_fuerza += np.random.randint(-1, 1) if np.random.rand() < 0.2 else 0
        genotipo_velocidad += np.random.randint(-1, 1) if np.random.rand() < 0.2 else 0
        genotipo_resistencia += np.random.randint(-1, 1) if np.random.rand() < 0.2 else 0
        genotipo_inteligencia += np.random.randint(-1, 1) if np.random.rand() < 0.2 else 0
        genotipo_adaptabilidad += np.random.randint(-1, 1) if np.random.rand() < 0.2 else 0
        genotipo_supervivencia += np.random.randint(-1, 1) if np.random.rand() < 0.2 else 0

        edad = 0
        salud = 100

        return [genotipo_fuerza, genotipo_velocidad, genotipo_resistencia, genotipo_inteligencia,
                genotipo_adaptabilidad, genotipo_supervivencia, edad, salud]

    def agregar_hijos(self, hijos):
        for hijo in hijos:
            self.genotipo_fuerza = np.append(self.genotipo_fuerza, hijo[0])
            self.genotipo_velocidad = np.append(self.genotipo_velocidad, hijo[1])
            self.genotipo_resistencia = np.append(self.genotipo_resistencia, hijo[2])
            self.genotipo_inteligencia = np.append(self.genotipo_inteligencia, hijo[3])
            self.genotipo_adaptabilidad = np.append(self.genotipo_adaptabilidad, hijo[4])
            self.genotipo_supervivencia = np.append(self.genotipo_supervivencia, hijo[5])
            self.edad = np.append(self.edad, hijo[6])
            self.edad_inicial = np.append(self.edad_inicial, hijo[6])
            self.salud = np.append(self.salud, hijo[7])
            self.hambre = np.append(self.hambre, 0)
            self.sed = np.append(self.sed, 0)
            self.cansancio = np.append(self.cansancio, 0)
            self.temperatura_corporal = np.append(self.temperatura_corporal, 37)
            self.genero = np.append(self.genero, np.random.choice(['masculino', 'femenino']))
            self.posiciones = np.append(self.posiciones,
                                        [[np.random.randint(0, self.tamano), np.random.randint(0, self.tamano)]],
                                        axis=0)
            self.ultima_reproduccion = np.append(self.ultima_reproduccion, -3)

    def mortalidad(self):
        prob_muerte = np.exp(0.01 * (self.hambre + self.sed + self.cansancio - 200))
        muerte = np.random.rand(self.n_humanos) < prob_muerte
        edad_muerte = self.edad >= np.random.normal(loc=75, scale=15, size=self.n_humanos)
        
        muerte |= edad_muerte

        return self.remove_humano(muerte)

    def remove_humano(self, muerte):
        self.hambre = self.hambre[~muerte]
        self.sed = self.sed[~muerte]
        self.cansancio = self.cansancio[~muerte]
        self.salud = self.salud[~muerte]
        self.temperatura_corporal = self.temperatura_corporal[~muerte]
        self.genotipo_fuerza = self.genotipo_fuerza[~muerte]
        self.genotipo_velocidad = self.genotipo_velocidad[~muerte]
        self.genotipo_resistencia = self.genotipo_resistencia[~muerte]
        self.genotipo_inteligencia = self.genotipo_inteligencia[~muerte]
        self.genotipo_adaptabilidad = self.genotipo_adaptabilidad[~muerte]
        self.genotipo_supervivencia = self.genotipo_supervivencia[~muerte]
        self.edad = self.edad[~muerte]
        self.edad_inicial = self.edad_inicial[~muerte]
        self.genero = self.genero[~muerte]
        self.ultima_reproduccion = self.ultima_reproduccion[~muerte]
        self.posiciones = self.posiciones[~muerte]

        muertos = np.sum(muerte)
        self.n_humanos -= muertos

        return muertos
