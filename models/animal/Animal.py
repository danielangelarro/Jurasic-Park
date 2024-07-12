from abc import ABC, abstractmethod


class Animal(ABC):
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
        self.objetos_en_area_vision = set()
        self.objetos_en_area_accion = set()
        self.posicion_en_area_accion = set()
        self.terreno_en_area_accion = set()
        self._ataque = ataque
        self._defensa = defensa
        self.habitat = habitat
        self.sed = 0
        self.cansancio = 0
        self.posicion = (0, 0)
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
        self.sobrevivir = 0

    def __str__(self):
        return (f'{self.especie} [{self.tipo}] \n'
                f'Peso: {self.peso} \n'
                f'Peso Maximo: {self.max_peso} \n'
                f'Posicion: {self.posicion} \n'
                f'Sexo: {self.sexo} \n'
                f'Sed: {self.sed} \n'
                f'Cansancio: {self.cansancio} \n'
                f'Edad: {self.edad} \n'
                f'Está vivo: {self.is_alive}')

    def __repr__(self):
        return str(self)

    def get_all_attributes(self):
        attributes = {}
        for cls in self.__class__.__mro__:
            for key, value in cls.__dict__.items():
                if isinstance(value, property):
                    attributes[key] = getattr(self, key)
                elif not key.startswith('__') and not key.endswith('__'):
                    attributes[key] = value
        attributes.update(self.__dict__)
        return attributes

    def set_posicion(self, x, y):
        self.posicion = (x, y)
