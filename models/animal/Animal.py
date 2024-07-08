import math
import random
from queue import SimpleQueue
from models.utils.Types_Enum import Etapa_Edad, Tipo_Terreno, Tipo_Entidad


class Animal:
    def __init__(self, especie, tipo, convivencia, peso, alcance_vision,
                 alcance_accion, ataque, defensa, habitat, sexo,
                 max_edad, time_gestacion, edad_adulta, huevo=False
                 ):
        self.especie = especie
        self.tipo = tipo
        self.convivencia = convivencia
        self.peso = peso / 4 if huevo else peso
        self.max_peso = peso
        self.min_peso = peso / 2
        self.alcance_vision = alcance_vision
        self.alcance_accion = alcance_accion
        self.__ataque = ataque
        self.__defensa = defensa
        self.habitat = habitat
        self.sed = 0
        self.cansancio = 0
        self.posicion = (0, 0)  # Agregamos posición
        self.sexo = sexo
        self.edad = -time_gestacion if huevo else max_edad // 2
        self.edad_adulta = edad_adulta
        self.max_edad = max_edad
        # self.ciclo_gestacion = -time_gestacion if huevo else 0
        self.time_gestacion = time_gestacion
        self.custodiando_huevo = False
        self.is_alive = True
        self.crias = []
        self.informacion_manada = set()

    def __str__(self):
        return (f'{self.especie} [{self.tipo}] \n'
                f'Peso: {self.peso} \n'
                f'Peso Maximo: {self.max_peso} \n'
                f'Posicion: {self.posicion} \n'
                f'Sexo: {self.sexo} \n'
                f'Sed: {self.sed} \n'
                f'Cansancio: {self.cansancio} \n'
                f'Edad: {self.edad} \n'
                f'Etapa edad: {self.get_etapa_edad}\n'
                f'Hambriento: {self.is_hambriento} \n'
                f'Está vivo: {self.is_alive}')

    def __repr__(self):
        return str(self)

    @property
    def is_hambriento(self):
        alpha = (self.min_peso + self.max_peso) / 2
        return self.peso <= alpha

    @property
    def is_sediento(self):
        return self.sed > 3

    def is_solo(self, ecosistema):
        objetos = self.objetos_en_area_vision(ecosistema)
        manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == self.especie]

        return manada == []

    @property
    def get_etapa_edad(self):
        if self.edad <= 0:
            return Etapa_Edad.HUEVO
        if self.edad < self.edad_adulta:
            return Etapa_Edad.JOVEN
        return Etapa_Edad.ADULTO

    def ataque(self, ecosistema, presa):
        atk = self.__ataque * 2 if self.custodiando_huevo else 1
        manada = [
            obj for obj in ecosistema.animales
            if obj.especie == self.especie and
               presa in obj.objetos_en_area_accion(ecosistema)
        ]
        atk += sum([m.__ataque * 0 if m.custodiando_huevo else 1 for m in manada])

        return atk

    def defensa(self, ecosistema):
        _defensa: float = self.__defensa
        objetos = self.objetos_en_area_accion(ecosistema)
        manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == self.especie]
        _defensa += sum([m.__ataque for m in manada])

        return _defensa

    def comprobar_informacion(self, ecosistema):
        objetos_visibles = [
            obj for obj in self.informacion_manada
            if self.posicion_en_area_vision(ecosistema, obj.posicion)
        ]
        for obj in objetos_visibles:
            self.informacion_manada.remove(obj)

    def set_posicion(self, x, y):
        self.posicion = (x, y)

    def posicion_en_area_vision(self, ecosistema, posicion):
        objetos = self.objetos_en_area_vision(ecosistema)
        posiciones = [obj.posicion for obj in objetos]

        return posicion in posiciones

    def posicion_en_area_accion(self, ecosistema):
        objetos = []

        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        visitados = set()

        queue = SimpleQueue()
        queue.put_nowait((self.posicion, 0))
        visitados.add(self.posicion)

        while not queue.empty():
            posicion, distancia = queue.get_nowait()

            for x, y in direcciones:
                nueva_posicion = (posicion[0] + x, posicion[1] + y)
                if (distancia <= self.alcance_accion and nueva_posicion not in visitados and
                        ecosistema.es_posicion_valida(nueva_posicion, self.habitat)):
                    entidad = ecosistema.entidades_en_posicion(nueva_posicion)
                    visitados.add(nueva_posicion)
                    objetos.append(nueva_posicion)

                    if not entidad or self.especie == "pteranodonte":
                        queue.put_nowait((nueva_posicion, distancia + 1))

        return objetos

    def objetos_en_area_accion(self, ecosistema):
        posiciones = self.posicion_en_area_accion(ecosistema)
        entidades = []

        for posicion in posiciones:
            entidades.extend(ecosistema.entidades_en_posicion(posicion))

        return entidades

    def terreno_en_area_accion(self, ecosistema):
        posiciones = self.posicion_en_area_accion(ecosistema)
        terrenos = []

        for posicion in posiciones:
            terrenos.append({
                "tipo": ecosistema.terreno_en_posicion(posicion),
                "posicion": posicion
            })

        return terrenos

    def objetos_en_area_vision(self, ecosistema, aumento=1):
        objetos = []

        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        visitados = set()

        queue = SimpleQueue()
        queue.put_nowait((self.posicion, 0))
        visitados.add(self.posicion)

        while not queue.empty():
            posicion, distancia = queue.get_nowait()

            for x, y in direcciones:
                nueva_posicion = (posicion[0] + x, posicion[1] + y)
                if (distancia <= self.alcance_vision * aumento and
                        nueva_posicion not in visitados and ecosistema.es_posicion_valida(nueva_posicion)):
                    visitados.add(nueva_posicion)
                    queue.put_nowait((nueva_posicion, distancia + 1))
                    objetos.extend(ecosistema.entidades_en_posicion(nueva_posicion))

        return objetos

    def crecer(self, ecosistema, reportes):
        self.peso -= 0.2

        if self.is_alive:
            self.edad += 1
            self.sed += 1

            if self.edad > self.max_edad:
                self.sed = 0
                self.is_alive = False
                reportes.append({
                    "entidad": self,
                    "tipo": "muerte",
                    "detalles": {
                        "causa": "edad"
                    }
                })

            if self.get_etapa_edad == Etapa_Edad.ADULTO and self.peso < self.min_peso:
                self.sed = 0
                self.is_alive = False
                reportes.append({
                    "entidad": self,
                    "tipo": "muerte",
                    "detalles": {
                        "causa": "hambre"
                    }
                })

            if self.sed > 7:
                self.sed = 0
                self.is_alive = False
                reportes.append({
                    "entidad": self,
                    "tipo": "muerte",
                    "detalles": {
                        "causa": "sed"
                    }
                })

        else:
            if self.get_etapa_edad != Etapa_Edad.HUEVO and self.peso <= 0:
                self.is_alive = False
                reportes.append({
                    "entidad": self,
                    "tipo": "muerte",
                    "detalles": {
                        "causa": "descomposicion"
                    }
                })
                ecosistema.animales.remove(self)

    def alimentarse(self):
        pass

    def beber(self, ecosistema, reportes):
        terrenos = self.terreno_en_area_accion(ecosistema)

        for terreno in terrenos:
            if terreno["tipo"] == Tipo_Terreno.AGUA:
                vecindades = ecosistema.posiciones_vecinas_libres(terreno["posicion"])

                for vecindad in vecindades:
                    if ecosistema.terreno_en_posicion(vecindad) != Tipo_Terreno.AGUA:
                        reportes.append({
                            "entidad": self,
                            "tipo": "beber",
                            "detalles": {
                                "acción": "tomar_agua",
                                "resultado": f"en ({vecindad[0]},{vecindad[1]})"
                            }
                        })
                        self.posicion = vecindad
                        self.sed = 0
                        return True

        self.acercarse_terreno(ecosistema, reportes, Tipo_Terreno.AGUA)
        return False

    def atacar(self, ecosistema, reportes):
        objetos = self.objetos_en_area_accion(ecosistema)
        presas = [
            obj for obj in objetos
            if obj.tipo == Tipo_Entidad.CARNIVORO and obj.especie != self.especie
               and obj.is_alive and self.ataque(ecosistema, obj) > obj.defensa(
                ecosistema)
        ]
        if presas:
            presa = random.choice(presas)
            presa.is_alive = False
            reportes.append({
                "entidad": self,
                "tipo": "atacar",
                "detalles": {
                    "acción": "atacar",
                    "presa": {
                        "especie": presa.especie,
                        "posicion": presa.posicion
                    },
                    "resultado_ataque": f"{self.ataque(ecosistema, presa)} vs {presa.defensa(ecosistema)}"
                }
            })
            return True
        return False

    def moverse(self, ecosistema, reportes):
        if self.custodiando_huevo:
            self.crias = [cria for cria in self.crias if cria is not None]
            huevo = [cria for cria in self.crias if cria.get_etapa_edad == Etapa_Edad.HUEVO]
            if huevo:
                return

        posiciones = self.posicion_en_area_accion(ecosistema)

        if posiciones:
            nueva_posicion = random.choice(posiciones)
            reportes.append({
                "entidad": self,
                "tipo": "moverse",
                "detalles": {
                    "acción": "moverse",
                    "resultado": f"a ({nueva_posicion[0]},{nueva_posicion[1]})"
                }
            })
            self.posicion = nueva_posicion

            return True
        return False

    def huir(self, ecosistema, reportes):
        objetos = self.objetos_en_area_vision(ecosistema, 2)
        posiciones = self.posicion_en_area_accion(ecosistema)
        predadores = [obj for obj in objetos if obj.tipo == Tipo_Entidad.CARNIVORO and obj.especie != self.especie]

        direccion = (self.posicion, 0)

        for posicion in posiciones:
            distance = 0
            for predador in predadores:
                distance += ecosistema.get_distance(posicion, predador.posicion)

            if direccion[1] < distance:
                direccion = (posicion, distance)

        if direccion[1] == 0:
            return False

        reportes.append({
            "entidad": self,
            "tipo": "huir",
            "detalles": {
                "acción": "huir",
                "resultado": f"a ({direccion[0][0]},{direccion[0][1]})"
            }
        })
        self.posicion = direccion[0]

        return True

    def acercarse_terreno(self, ecosistema, reportes, terrenos):

        objetos = self.objetos_en_area_vision(ecosistema)
        posiciones_vision = [obj.posicion for obj in objetos]

        posiciones = self.posicion_en_area_accion(ecosistema)
        posiciones = [pos for pos in posiciones_vision if ecosistema.terreno_en_posicion(pos) in [terrenos]]

        direccion = (self.posicion, math.inf)

        for posicion in posiciones:
            distance = 0
            for pos_vision in posiciones_vision:
                distance += ecosistema.get_distance(posicion, pos_vision)

            if direccion[1] > distance:
                direccion = (posicion, distance)

        if direccion[1] == math.inf:
            return False

        reportes.append({
            "entidad": self,
            "tipo": "acercarse",
            "detalles": {
                "acción": "acercarse",
                "terrenos": str(terrenos),
                "direccion": direccion,
                "resultado": f"a ({direccion[0][0]},{direccion[0][1]})"
            }
        })
        self.posicion = direccion[0]

        return True

    def acercarse(self, ecosistema, reportes, aumento = 2, especie=None):
        if not self.is_solo(ecosistema):
            return False

        if especie is None:
            especie = self.especie

        objetos = self.objetos_en_area_vision(ecosistema, aumento)
        posiciones = self.posicion_en_area_accion(ecosistema)
        manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == especie]

        direccion = (self.posicion, math.inf)

        for posicion in posiciones:
            distance = 0
            for entidad in manada:
                distance += ecosistema.get_distance(posicion, entidad.posicion)

            if direccion[1] > distance:
                direccion = (posicion, distance)

        if direccion[1] == math.inf:
            return False

        reportes.append({
            "entidad": self,
            "tipo": "acercarse",
            "detalles": {
                "acción": "acercarse",
                "especie": especie,
                "direccion": direccion,
                "resultado": f"a ({direccion[0][0]},{direccion[0][1]})"
            }
        })
        self.posicion = direccion[0]

        return True

    def gritar(self, ecosistema, reportes):
        if not self.is_solo(ecosistema):
            return False

        objetos = self.objetos_en_area_vision(ecosistema, 2)
        manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == self.especie]

        if manada:
            map(lambda x: x.informacion_manada.union(self), manada)
            reportes.append({
                "entidad": self,
                "tipo": "gritar",
                "detalles": {
                    "acción": "gritar",
                    "resultado": "perdido"
                }
            })
            return True
        return False

    def comunicar(self, ecosistema, reportes):
        objetos = self.objetos_en_area_vision(ecosistema)
        informacion = set()

        algo_que_comunicar = False
        for obj in objetos:
            if isinstance(obj, Animal):
                if self.tipo == "herbivoro" and obj.tipo == Tipo_Entidad.CARNIVORO:
                    informacion.add(obj)
                    algo_que_comunicar = True
                    reportes.append({
                        "entidad": self,
                        "tipo": "comunicar",
                        "detalles": {
                            "acción": "ver",
                            "objeto": obj.especie,
                            "posicion": obj.posicion,
                            "resultado": "peligro"
                        }
                    })
                elif self.tipo == Tipo_Entidad.CARNIVORO and obj.tipo == "herbivoro":
                    informacion.add(obj)
                    algo_que_comunicar = True
                    reportes.append({
                        "entidad": self,
                        "tipo": "comunicar",
                        "detalles": {
                            "acción": "ver",
                            "objeto": obj.especie,
                            "posicion": obj.posicion,
                            "resultado": "comida"
                        }
                    })

        if not algo_que_comunicar:
            return False

        manada = [obj for obj in objetos if isinstance(obj, Animal) and obj.especie == self.especie]
        if manada:
            map(lambda x: x.informacion_manada.union(informacion), manada)
            return True
        return False

    def aparearse(self, ecosistema, reportes):
        if self.sexo == "Macho" and self.edad >= self.edad_adulta:
            objetos = self.objetos_en_area_accion(ecosistema)
            animales = [obj for obj in objetos if isinstance(obj, Animal)]
            hembras = [
                obj for obj in animales
                if obj.especie == self.especie
                   and obj.sexo == "Hembra"
                   and obj.edad >= self.edad_adulta
                   and not obj.custodiando_huevo
                   and ecosistema.posiciones_vecinas_libres(obj.posicion)
            ]
            if hembras:
                hembra = hembras[0]
                posiciones_vecinas = ecosistema.posiciones_vecinas_libres(hembra.posicion)
                posicion_huevo = random.choice(posiciones_vecinas)
                nuevo_huevo = self.__class__(sexo=random.choice(["Macho", "Hembra"]), huevo=True)
                nuevo_huevo.set_posicion(posicion_huevo[0], posicion_huevo[1])
                ecosistema.animales.append(nuevo_huevo)
                hembra.custodiando_huevo = True
                hembra.crias.append(nuevo_huevo)
                reportes.append({
                    "entidad": self,
                    "tipo": "aparearse",
                    "detalles": {
                        "acción": "aparearse",
                        "resultado": f"[Huevo en ({posicion_huevo[0]},{posicion_huevo[1]})]"
                    }
                })

                return True
        return False

    def decidir_accion(self, ecosistema, reportes):
        pass
