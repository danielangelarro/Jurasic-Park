import numpy as np
from experta import *


# Definimos un hecho para el estado de la comunidad
class EstadoComunidad(Fact):
    """Representa el estado fisiológico y la necesidad de recursos de la comunidad"""
    sed = Field(float)
    hambre = Field(float)
    cansancio = Field(float)
    permitir_reproduccion = Field(bool)


# Sistema experto que define las reglas para la selección de acciones
class SistemaExperto(KnowledgeEngine):
    def __init__(self, comunidad, entorno):
        super().__init__()
        self.comunidad = comunidad
        self.entorno = entorno

    @Rule(EstadoComunidad(sed=P(lambda sed: sed > 0)))
    def decidir_buscar_agua(self):
        resultado = self.comunidad.buscar_agua(self.entorno)

    @Rule(EstadoComunidad(hambre=P(lambda hambre: hambre > 0)))
    def decidir_buscar_comida(self):
        resultado = self.comunidad.buscar_comida(self.entorno)

    @Rule(EstadoComunidad(cansancio=P(lambda cansancio: cansancio > 0)))
    def decidir_descansar(self):
        resultado = self.comunidad.descansar()
    
    @Rule(EstadoComunidad(permitir_reproduccion=True))
    def decidir_reproducir(self):
        resultado = self.comunidad.reproducirse()
