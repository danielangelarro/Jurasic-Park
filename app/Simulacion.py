import random

import matplotlib.pyplot as plt
from collections import Counter

from app.Ecosistema import Ecosistema
from models.humano.Humano import Humano
from models.utils.Evento import Evento


class Simulacion:
    def __init__(self, ecosistema):
        self.ecosistema = ecosistema
        self.total_humanos = 0
        self.total_nacimientos = 0
        self.total_acciones_realizadas = 0
        self.edad_promedio_muerte = []
        self.acciones_por_tipo = {accion: 0 for accion in ["cazar", "recolectar", "pescar", "descansar", "construir", "buscar_refugio", "huir", "comunicar", "aparearse", "acercarse", "gritar", "moverse", "beber", "atacar"]}
        self.exitos_por_accion = {accion: 0 for accion in self.acciones_por_tipo}
        self.fracasos_por_accion = {accion: 0 for accion in self.acciones_por_tipo}
        self.niveles_promedios = {"hambre": [], "sed": [], "cansancio": []}
        self.humanos_por_area = {area: 0 for area in ["sabana", "desierto", "pradera", "agua", "acantilado", "pantano"]}
        self.experimentos = []
        self.historial = []

    def agregar_humano(self, humano):
        self.ecosistema.agregar_animal(humano)
        self.ecosistema.total_humanos += 1
        self.total_humanos += 1

    def registrar_accion(self, accion, exito=True):
        self.total_acciones_realizadas += 1
        self.acciones_por_tipo[accion] += 1
        if exito:
            self.exitos_por_accion[accion] += 1
        else:
            self.fracasos_por_accion[accion] += 1

    def registrar_muerte(self, entidad):
        self.edad_promedio_muerte.append(entidad.edad)

    def registrar_eventos(self, reportes):
        for reporte in reportes:
            tiempo = self.ecosistema.days
            entidad = reporte["entidad"]
            especie = entidad.especie
            posicion = entidad.posicion
            mensaje = ""

            if reporte["tipo"] == "muerte":
                causa = reporte["detalles"]["causa"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) muere por causa ({causa})."
            elif reporte["tipo"] == "tomar_agua":
                vecindad = reporte["detalles"]["vecindad"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) toma agua en ({vecindad[0]},{vecindad[1]})"
            elif reporte["tipo"] == "ataque":
                presa = reporte["detalles"]["presa"]
                resultado_ataque = reporte["detalles"]["resultado_ataque"]
                defensa_presa = presa.defensa(self.ecosistema)
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ataca {presa.especie} ({presa.posicion[0]},{presa.posicion[1]}) [{resultado_ataque} vs {defensa_presa}]"
            elif reporte["tipo"] == "movimiento":
                nueva_posicion = reporte["detalles"]["nueva_posicion"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) se mueve a ({nueva_posicion[0]},{nueva_posicion[1]})"
            elif reporte["tipo"] == "alimentarse":
                comida = reporte["detalles"]["comida"]
                peso = reporte["detalles"]["peso"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) a comido ({comida}), peso actual ({peso})"
            elif reporte["tipo"] == "huir":
                direccion = reporte["detalles"]["direccion"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) huye a ({direccion[0][0]},{direccion[0][1]})"
            elif reporte["tipo"] == "acercarse":
                direccion = reporte["detalles"]["direccion"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) se acerca a ({direccion[0][0]},{direccion[0][1]})"
            elif reporte["tipo"] == "grito":
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) lanza grito [perdido]"
            elif reporte["tipo"] == "peligro":
                obj = reporte["detalles"]["obj"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ve a {obj.especie} ({obj.posicion[0]},{obj.posicion[1]}) [peligro]"
            elif reporte["tipo"] == "comida":
                obj = reporte["detalles"]["obj"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ve a {obj.especie} ({obj.posicion[0]},{obj.posicion[1]}) [comida]"
            elif reporte["tipo"] == "apareamiento":
                hembra = reporte["detalles"]["hembra"]
                posicion_huevo = reporte["detalles"]["posicion_huevo"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) se aparea con {hembra.especie} ({hembra.posicion[0]},{hembra.posicion[1]}) [Huevo en ({posicion_huevo[0]},{posicion_huevo[1]})]"
            elif reporte["tipo"] == "consumo_animal":
                presa = reporte["detalles"]["presa"]
                cantidad_comida = reporte["detalles"]["cantidad_comida"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) come {presa.especie} ({presa.posicion[0]},{presa.posicion[1]}) [{cantidad_comida} T]"
            elif reporte["tipo"] == "consumo_planta":
                planta = reporte["detalles"]["planta"]
                cantidad_comida = reporte["detalles"]["cantidad_comida"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) come {planta.tipo} ({planta.posicion[0]},{planta.posicion[1]}) [{cantidad_comida} T]"
            elif reporte["tipo"] == "descanso":
                nivel_cansancio = reporte["detalles"]["nivel_cansancio"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ha descansado. Nivel de cansancio: {nivel_cansancio}."
            elif reporte["tipo"] == "caza":
                comida_obtenida = reporte["detalles"]["comida_obtenida"]
                nueva_habilidad_caza = reporte["detalles"]["nueva_habilidad_caza"]
                nivel_peso = reporte["detalles"]["nivel_peso"]
                nivel_cansancio = reporte["detalles"]["nivel_cansancio"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) caza. Comida obtenida: {comida_obtenida}. Nueva habilidad de caza: {nueva_habilidad_caza}. Nivel de peso: {nivel_peso}. Nivel de cansancio: {nivel_cansancio}."
            elif reporte["tipo"] == "recoleccion":
                recursos_obtenidos = reporte["detalles"]["recursos_obtenidos"]
                nueva_habilidad_recoleccion = reporte["detalles"]["nueva_habilidad_recoleccion"]
                nivel_peso = reporte["detalles"]["nivel_peso"]
                nivel_cansancio = reporte["detalles"]["nivel_cansancio"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ha recolectado. Recursos obtenidos: {recursos_obtenidos}. Nueva habilidad de recolección: {nueva_habilidad_recoleccion}. Nivel de peso: {nivel_peso}. Nivel de cansancio: {nivel_cansancio}."
            elif reporte["tipo"] == "pesca":
                peces_obtenidos = reporte["detalles"]["peces_obtenidos"]
                nueva_habilidad_pesca = reporte["detalles"]["nueva_habilidad_pesca"]
                nivel_peso = reporte["detalles"]["nivel_peso"]
                nivel_cansancio = reporte["detalles"]["nivel_cansancio"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ha pescado. Peces obtenidos: {peces_obtenidos}. Nueva habilidad de pesca: {nueva_habilidad_pesca}. Nivel de peso: {nivel_peso}. Nivel de cansancio: {nivel_cansancio}."
            elif reporte["tipo"] == "apareamiento_iniciado":
                pareja = reporte["detalles"]["pareja"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) se aparea con {pareja.especie} ({pareja.posicion[0]},{pareja.posicion[1]}) [Embarazo iniciado]"
            elif reporte["tipo"] == "embarazo_iniciado":
                pareja = reporte["detalles"]["pareja"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) se aparea con {pareja.especie} ({pareja.posicion[0]},{pareja.posicion[1]}) [Embarazo iniciado]"
            elif reporte["tipo"] == "nacimiento":
                nuevo_bebe = reporte["detalles"]["nuevo_bebe"]
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) ha dado a luz a un bebé ({nuevo_bebe.sexo}) [Bebé en ({posicion[0]},{posicion[1]})]"

            evento = Evento(tiempo=tiempo, entidad=entidad, tipo=reporte["tipo"], mensaje=mensaje, detalles=reporte["detalles"])
            self.historial.append(evento)

        self.historial_humanos.append(len([a for a in self.ecosistema.animales if isinstance(a, Humano)]))

    def imprimir_historial_eventos(self):
        for evento in self.historial:
            print(evento)

    def obtener_eventos_por_tipo(self, tipo):
        return [evento for evento in self.historial if evento.tipo == tipo]

    def obtener_eventos_por_entidad(self, entidad):
        return [evento for evento in self.historial if evento.entidad == entidad]

    def obtener_eventos_por_tipo_y_especie(self,  tipo, especie):
        return [evento for evento in self.historial if evento.entidad.especie == especie and evento.tipo == tipo]

    def actualizar_estado_fisiologico(self, hambre, sed, cansancio):
        self.niveles_promedios["hambre"].append(hambre)
        self.niveles_promedios["sed"].append(sed)
        self.niveles_promedios["cansancio"].append(cansancio)

    def realizar_experimento(self, nombre, func, *args, **kwargs):
        resultado = func(*args, **kwargs)
        self.experimentos.append((nombre, resultado))

    def evaluar_simulacion(self, dias_simulacion):
        self.total_humanos += self.total_nacimientos

        dias = self.ecosistema.days / dias_simulacion
        humanos_sobrevivientes = len(self.ecosistema.humanos) / self.total_humanos

        return dias + humanos_sobrevivientes

    def graficar_historial(self):

        dias = self.ecosistema.days

        fig, ax = plt.subplots()
        ax.plot(range(len(dias)), dias)

        ax.set_title('Cantidad de humanos por día')
        ax.set_xlabel('Día')
        ax.set_ylabel('Cantidad de Humanos')
        ax.grid(True)

        plt.show()

    def reset_simulacion(self):
        self.ecosistema.reset()
        self.total_humanos = 0
        self.total_nacimientos = 0
        self.total_muertes = 0
        self.total_acciones_realizadas = 0
        self.edad_promedio_muerte = []
        self.acciones_por_tipo = {accion: 0 for accion in
                                  ["cazar", "recolectar", "pescar", "descansar", "construir", "buscar_refugio", "huir",
                                   "comunicar", "aparearse", "acercarse", "gritar", "moverse", "beber", "atacar"]}
        self.exitos_por_accion = {accion: 0 for accion in self.acciones_por_tipo}
        self.fracasos_por_accion = {accion: 0 for accion in self.acciones_por_tipo}
        self.niveles_promedios = {"hambre": [], "sed": [], "cansancio": []}
        self.humanos_por_area = {area: 0 for area in ["sabana", "desierto", "pradera", "agua", "acantilado", "pantano"]}
        self.experimentos = []
        self.historial = []
        self.historial_humanos = []

        # Agregar humanos al ecosistema
        for i in range(10):  # Por ejemplo, agregamos 10 humanos para iniciar
            humano = Humano(
                nombre=f"Humano {i + 1}",
                edad=random.randint(20, 50),
                sexo=random.choice(["Macho", "Hembra"]),
                personalidad=random.choice(["Cazador", "Recolector", "Explorador"])
            )
            self.agregar_humano(humano)

    def experimento_supervivencia(self):
        # Ejecutar simulación por un número determinado de días
        dias_simulacion = 72000 # 200 anios
        num_generaciones = 5

        for generacion in range(num_generaciones):
            self.reset_simulacion()

            for _ in range(dias_simulacion):
                reportes = self.ecosistema.ciclo()

                if not len(self.ecosistema.humanos):
                    break

                print(f"Cantidad de eventos: {len(reportes)}")

                # for evento in reportes:
                #     if not isinstance(evento["entidad"], Humano):
                #         continue

            print(f"Generación {generacion + 1}:"
                  f"Evaluación: {self.evaluar_simulacion(self.ecosistema.days)} pts\n"
                  f"Duración de días: {self.ecosistema.days}/{dias_simulacion}\n"
                  f"Sobrevivientes: {len(self.ecosistema.humanos)}/{self.total_humanos}\n")

            self.ecosistema.evolucionar()
