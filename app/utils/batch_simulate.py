from app.utils.simulacion import Simulacion


def batch_simulate(
        n_simulations,
        tamano_entorno=10,
        n_humanos=10,
        n_ciclos=100,
        genotipo={},
        dinosaurios=[],
        reproduccion=True,
        entorno=None
):
    batch_poblacion = []

    for _ in range(n_simulations):        
        simulacion = Simulacion(
            tamano_entorno=tamano_entorno,
            n_humanos=n_humanos,
            n_ciclos=n_ciclos,
            genotipo=genotipo,
            reproduccion=reproduccion,
            dinosaurios=dinosaurios,
            entorno=entorno
        )
        results = simulacion.ejecutar()
        batch_poblacion.append(results)

    return batch_poblacion
