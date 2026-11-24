from app.prompts.prompt_library import PROMPT_TEMPLATES

def generar_prompt(nombre: str, datos: dict) -> str:

    #verificar que la plantilla exista:
    if nombre not it PROMPT_TEMPLATES:
        raise ValueError("La plantilla solicitada no existe")

    plantilla = PROMPT_TEMPLATES[nombre]

    # Completamos los espacios dinámicos
    prompt = plantilla.format(**datos)

    return prompt