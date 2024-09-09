import random

from app.Ecosistema import Ecosistema
from app.Simulacion import Simulacion
from app.utils_map import cargar_mapa


# Cargar el mapa
mapa = cargar_mapa()

# Crear la simulacion
ecosistema = Ecosistema(mapa)
simulacion = Simulacion(ecosistema)

# for _ in range(5):
#     ecosistema.agregar_animal(Braquiosaurio(sexo=random.choice(["Macho", "Hembra"])))
#
# for _ in range(7):
#     ecosistema.agregar_animal(Triceratops(sexo=random.choice(["Macho", "Hembra"])))

# for _ in range(7):
#     ecosistema.agregar_animal(Tiranosaurio(sexo=random.choice(["Macho", "Hembra"])))

# for _ in range(3):
#     ecosistema.agregar_vegetacion(secuoya)
#
# for _ in range(5):
#     ecosistema.agregar_vegetacion(helecho)
#
# for _ in range(5):
#     ecosistema.agregar_vegetacion(baya)

#
# for i in range(5):
#     simulacion.agregar_humano(Humano(
#         nombre=f"Arthur {i+1}",
#         edad=random.randint(20, 30),
#         sexo=random.choice(["Macho", "Hembra"]),
#         personalidad=random.choice(["Cazador", "Recolector", "Explorador"])
#     ))

# # Ejecutar ciclos de simulación
# for ciclo in range(360):
#     # print(f"Ciclo {ciclo}")
#     reportes = ecosistema.ciclo()
#     # for reporte in reportes:
#     #     print(reporte)
#
# print("\n", "=" * 20)
# ecosistema.imprimir_estados()

# Realizar experimentos
simulacion.realizar_experimento("Supervivencia", simulacion.experimento_supervivencia)
# print("="*20)
# simulacion.imprimir_historial_eventos()

# Graficar historial de la simulación
# simulacion.graficar_historial()
