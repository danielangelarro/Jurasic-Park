class Evento:
    def __init__(self, tiempo, entidad, tipo, detalles=None, exito=True):
        self.tiempo = tiempo
        self.entidad = entidad
        self.tipo = tipo
        self.detalles = detalles or {}
        self.exito = exito

    def __str__(self):
        return f"Tiempo: {self.tiempo}, Entidad: {self.entidad}, Tipo: {self.tipo}, Detalles: {self.detalles}"
