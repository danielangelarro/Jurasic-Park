from enum import Enum


class Etapa_Edad(Enum):
    HUEVO = 0
    JOVEN = 1
    ADULTO = 2


class Tipo_Entidad(Enum):
    CARNIVORO = 0
    HERBIVORO = 1
    VEGETAL = 2
    MIXTO = 3

class Tipo_Terreno(Enum):
    ALL = 0
    SABANA = 1
    DESIERTO = 2
    ACANTILADO = 3
    PANTANO = 4
    AGUA = 5
    PRADERA = 6


class Accion_Animal(Enum):
    BEBER = 0
    CRECER = 1
    ALIMENTARSE = 2
    ATACAR = 3
    MOVERSE = 4
    HUIR = 5
    ACERCARSE_MANADA = 6
    GRITAR = 7
    COMUNICAR = 8
    APAREARSE = 9
