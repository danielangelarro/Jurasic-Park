import random

import matplotlib.pyplot as plt

from app.Ecosistema import Ecosistema
from models.humano.Humano import Humano
from models.utils.Evento import Evento


class Simulacion:
    def __init__(self, ecosistema):
        self.ecosistema = ecosistema
        self.total_humanos = 0
        self.total_nacimientos = 0
        self.total_muertes = 0
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
        self.total_humanos += 1
        # self.humanos_por_area[humano.area] += 1

    def registrar_accion(self, accion, exito=True):
        self.total_acciones_realizadas += 1
        self.acciones_por_tipo[accion] += 1
        if exito:
            self.exitos_por_accion[accion] += 1
        else:
            self.fracasos_por_accion[accion] += 1

    def registrar_muerte(self, entidad):
        self.total_muertes += 1
        self.edad_promedio_muerte.append(entidad.edad)

    def registrar_eventos(self, reportes):
        for reporte in reportes:
            tiempo = self.ecosistema.days
            entidad = reporte["entidad"]
            especie = entidad.especie
            posicion = entidad.posicion

            if reporte["tipo"] == "muerte":
                mensaje = f"{especie} ({posicion[0]},{posicion[1]}) muere."
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

            evento = Evento(tiempo=tiempo, entidad=entidad, tipo=reporte["tipo"], detalles=reporte["detalles"])
            self.historial.append(evento)

    def actualizar_estado_fisiologico(self, hambre, sed, cansancio):
        self.niveles_promedios["hambre"].append(hambre)
        self.niveles_promedios["sed"].append(sed)
        self.niveles_promedios["cansancio"].append(cansancio)

    def realizar_experimento(self, nombre, func, *args, **kwargs):
        resultado = func(*args, **kwargs)
        self.experimentos.append((nombre, resultado))

    def imprimir_estadisticas(self):
        print(f"Total de humanos: {self.total_humanos}")
        print(f"Total de nacimientos: {self.total_nacimientos}")
        print(f"Total de muertes: {self.total_muertes}")
        print(f"Total de acciones realizadas: {self.total_acciones_realizadas}")
        print(f"Edad promedio de muerte: {sum(self.edad_promedio_muerte)/len(self.edad_promedio_muerte) if self.edad_promedio_muerte else 0}")
        print(f"Acciones por tipo: {self.acciones_por_tipo}")
        print(f"Exitos por accion: {self.exitos_por_accion}")
        print(f"Fracasos por accion: {self.fracasos_por_accion}")
        print(f"Niveles promedios de hambre: {sum(self.niveles_promedios['hambre'])/len(self.niveles_promedios['hambre']) if self.niveles_promedios['hambre'] else 0}")
        print(f"Niveles promedios de sed: {sum(self.niveles_promedios['sed'])/len(self.niveles_promedios['sed']) if self.niveles_promedios['sed'] else 0}")
        print(f"Niveles promedios de cansancio: {sum(self.niveles_promedios['cansancio'])/len(self.niveles_promedios['cansancio']) if self.niveles_promedios['cansancio'] else 0}")
        print(f"Humanos por area: {self.humanos_por_area}")

    def graficar_historial(self):
        dias = [evento.tiempo for evento in self.historial if isinstance(evento.entidad, Humano)]
        acciones = [evento.tipo for evento in self.historial if isinstance(evento.entidad, Humano)]

        plt.figure(figsize=(10, 5))
        plt.hist(dias, bins=max(dias), alpha=0.5, label="Días")
        plt.xticks(range(min(dias), max(dias) + 1))
        plt.xlabel("Día")
        plt.ylabel("Cantidad de Eventos")
        plt.title("Historial de Eventos por Día")
        plt.legend()
        plt.show()

        plt.figure(figsize=(10, 5))
        plt.hist(acciones, bins=len(set(acciones)), alpha=0.5, label="Acciones")
        plt.xticks(rotation=90)
        plt.xlabel("Acción")
        plt.ylabel("Cantidad de Eventos")
        plt.title("Historial de Acciones Realizadas")
        plt.legend()
        plt.show()

    def experimento_supervivencia(self):
        # Reiniciar el ecosistema para un nuevo experimento
        self.ecosistema = Ecosistema(self.ecosistema.mapa)
        self.total_humanos = 0
        self.total_nacimientos = 0
        self.total_muertes = 0
        self.total_acciones_realizadas = 0
        self.edad_promedio_muerte = []
        self.acciones_por_tipo = {accion: 0 for accion in ["cazar", "recolectar", "pescar", "descansar", "construir", "buscar_refugio", "huir", "comunicar", "aparearse", "acercarse", "gritar", "moverse", "beber", "atacar"]}
        self.exitos_por_accion = {accion: 0 for accion in self.acciones_por_tipo}
        self.fracasos_por_accion = {accion: 0 for accion in self.acciones_por_tipo}
        self.niveles_promedios = {"hambre": [], "sed": [], "cansancio": []}
        self.humanos_por_area = {area: 0 for area in ["sabana", "desierto", "pradera", "agua", "acantilado", "pantano"]}
        self.experimentos = []
        self.historial = []

        # Agregar humanos al ecosistema
        for i in range(10):  # Por ejemplo, agregamos 10 humanos para iniciar
            humano = Humano(
                nombre=f"Humano {i+1}",
                edad=random.randint(20, 50),
                sexo=random.choice(["Macho", "Hembra"]),
                personalidad=random.choice(["Cazador", "Recolector", "Explorador"])
            )
            self.agregar_humano(humano)

        # Ejecutar simulación por un número determinado de días
        dias_simulacion = 100
        for _ in range(dias_simulacion):
            reportes = self.ecosistema.ciclo()
            self.registrar_eventos(reportes)

            for evento in reportes:
                if not isinstance(evento["entidad"], Humano):
                    continue

                if evento["tipo"] == "muerte":
                    self.registrar_muerte(evento["entidad"])
                elif evento["tipo"] in self.acciones_por_tipo:
                    exito = evento["detalles"]["resultado"]  # Si el evento tiene éxito o no
                    self.registrar_accion(evento["tipo"], exito)

            # Actualizar niveles promedios de hambre, sed y cansancio
            niveles_hambre = [humano.is_hambriento for humano in self.ecosistema.animales if isinstance(humano, Humano)]
            niveles_sed = [humano.is_sediento for humano in self.ecosistema.animales if isinstance(humano, Humano)]
            niveles_cansancio = [humano.cansancio for humano in self.ecosistema.animales if isinstance(humano, Humano)]
            if niveles_hambre and niveles_sed and niveles_cansancio:
                self.actualizar_estado_fisiologico(sum(niveles_hambre) / len(niveles_hambre), sum(niveles_sed) / len(niveles_sed), sum(niveles_cansancio) / len(niveles_cansancio))

        # Finalización del experimento
        self.imprimir_estadisticas()
