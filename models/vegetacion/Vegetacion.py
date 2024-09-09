import random

from models.Entidad import Entidad
from models.utils.Types_Enum import Tipo_Entidad, Tipo_Terreno


class Vegetacion(Entidad):
    def __init__(self, especie, frutal, peso, max_peso, edad, edad_adulta, alcance, habitat):
        super().__init__(especie, peso, edad, habitat)

        self.frutal = frutal
        self.tipo = Tipo_Entidad.VEGETAL
        self.min_peso = max_peso * 0.2
        self.max_peso = max_peso
        self.edad_adulta = edad_adulta
        self.alcance = alcance

    @property
    def adulto(self):
        return self.edad >= self.edad_adulta

    def set_posicion(self, x, y):
        self.posicion = (x, y)

    def crecer(self, ecosistema, reportes):
        self.peso += 1 if self.is_alive else -1
        self.peso = min(self.peso, self.max_peso)

        if self.is_alive:
            self.edad += 1

        if self.edad == self.adulto:
            x, y = self.posicion
            posiciones = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ]

            entidades = []
            for pos in posiciones:
                entidades.extend(ecosistema.entidades_en_posicion(pos))

            plantas_jovenes = [
                obj for obj in entidades
                if obj.tipo == Tipo_Entidad.VEGETAL
            ]

            for pj in plantas_jovenes:
                pj.is_alive = False

        if self.peso <= 0:
            reportes.append({
                "entidad": self,
                "tipo": "muerte",
                "detalles": {}
            })
            ecosistema.vegetacion.remove(self)

    def posiciones_vacias_en_area_accion(self, ecosistema):
        posiciones = []
        for x in range(-self.alcance, self.alcance + 1):
            for y in range(-self.alcance, self.alcance + 1):
                nueva_posicion = (self.posicion[0] + x, self.posicion[1] + y)
                if ecosistema.es_posicion_valida(nueva_posicion) and ecosistema.entidades_en_posicion(
                        nueva_posicion) == []:
                    posiciones.append(nueva_posicion)
        return posiciones

    def reproducir(self, ecosistema):
        posiciones = self.posiciones_vacias_en_area_accion(ecosistema)
        posiciones = [p for p in posiciones if ecosistema.terreno_en_posicion(p) == Tipo_Terreno.PRADERA]

        if posiciones == []:
            return

        nueva_posicion = random.choices(posiciones)
        ecosistema.agregar_vegetacion(Vegetacion(
            self.tipo,
            self.peso,
            self.alcance,
            nueva_posicion[0],
            nueva_posicion[1]
        ))
