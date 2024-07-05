# Chat with an intelligent assistant in your terminal
from openai import OpenAI

# Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")



# Define las acciones y zonas posibles
acciones = [
    "explorar", "cazar", "recolectar", "pescar", "descansar",
    "socializar", "construir", "defenderse", "buscar refugio", "buscar agua", "buscar comida"
]

zonas = ["Bosque", "Desierto", "Pantano", "Sabana", "Montaña"]

def generar_arbol_decisiones(personalidad, zona, contexto, acciones):
    acciones_str = ", ".join(acciones)
    prompt = (
        f"Genera un árbol de decisiones para un humano con personalidad '{personalidad}' que se encuentra en la zona '{zona}' "
        f"y en la siguiente situación: {contexto}. "
        f"El humano puede realizar las siguientes acciones: {acciones_str}. "
        "Genera un árbol de decisiones detallado para determinar las acciones prioritarias basadas en su personalidad y situación."
    )

    # print(prompt)
    return prompt

    history = [
        {"role": "system",
         "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "user",
         "content": prompt},
    ]

    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=history,
        temperature=0.7,
        stream=True,
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    return new_message["content"]


# Ejemplo de uso
zona = "Bosque"
contexto = "El humano tiene hambre y sed, y hay depredadores cerca. También hay una fuente de agua y algunos arbustos con bayas comestibles en las cercanías."
personalidad = "Explorador"
arbol_decisiones = generar_arbol_decisiones(personalidad, zona, contexto, acciones)
print(f"Árbol de decisiones para un {personalidad} en {zona}:\n{arbol_decisiones}\n")
