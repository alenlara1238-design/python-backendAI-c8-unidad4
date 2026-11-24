PROMPT_TEMPLATES = {
    "respuesta_soporte": """
        Actúa como un agente profesional de soporte de Nexus Nexus SAS.
        Debes responder la siguiente consulta de un cliente:
        {consulta}

        Genera una respuesta que cumpla estas condiciones:
        - Utiliza un lenguaje amable y profesional.
        - Explica la situación de manera clara.
        - Propón pasos para solucionar el problema.
        - No inventes funcionalidades ni información comercial.
        - Si no tienes información suficiente, indícarlo.
        - Evitar inventar características no documentadas.
    """,
    "seguimiento_cliente": """
        Actúa como un agente de Atención al Cliente de Nexus Saas.
        Debes redactar un mensaje de seguimiento considerando la siguiente situación:

        {situacion}

        El mensaje debe:
        - Ser profesional y cordial.
        - Mostrar interés por el caso del cliente.
        - Comunicar claramente los próximos pasos.
        - Evitar prometer resultados o tiempos no confirmados.
    """


}