# Módulo 3. Generador de correos electrónicos con IA

Debes desarrollar una funcionalidad que permita a los empleados de soporte de Nexus SaaS generar correos electrónicos profesionales utilizando inteligencia artificial.

El usuario proporcionará información básica sobre el mensaje que necesita redactar y Gemini generará una propuesta de correo.

**Importante:** En esta versión, la aplicación solamente generará el contenido del correo. No realizará envíos.

## 2. Comportamiento esperado

Imaginemos que un empleado de soporte necesita informar a un cliente que su solicitud fue recibida y está siendo revisada.

El empleado proporcionará información como:

- Destinatario: Carlos Rodríguez.
- Motivo: Confirmación de recepción de solicitud.
- Detalles: El equipo técnico está revisando el inconveniente con el acceso a su cuenta.
- Tono: Profesional y cordial.

La IA deberá generar una propuesta similar a esta:

**Asunto:** Confirmación de recepción de su solicitud

**Cuerpo:**

Estimado Carlos:

Le confirmamos que hemos recibido su solicitud relacionada con el acceso a su cuenta de Nexus SaaS.

Nuestro equipo técnico se encuentra revisando el inconveniente para identificar su causa y determinar los pasos necesarios para solucionarlo.

Agradecemos su paciencia y comprensión.

Cordialmente,  
Equipo de Soporte Nexus SaaS

Este resultado es ilustrativo. El contenido definitivo será generado por Gemini.

---

## 3. Estructura del módulo

Trabajaremos con dos archivos nuevos pero sobre el mimo proyecto desarrollado en la clase 3:

```text
app/
│
├── prompts/
│   └── email_prompts.py
│
├── services/
│   └── email_service.py
│
└── main.py
```

Cada archivo tendrá una responsabilidad:

| Archivo            | Responsabilidad                                      |
| ------------------ | ---------------------------------------------------- |
| `email_prompts.py` | Definir las instrucciones que recibirá Gemini.       |
| `email_service.py` | Comunicarse con Gemini y procesar su respuesta.      |
| `main.py`          | Recibir los datos del usuario y exponer el endpoint. |

Las rutas continuarán centralizadas en `main.py`, como en los módulos anteriores.

---

# Parte 1. Crear el prompt para los correos

## Paso 1. Crear el archivo `email_prompts.py`

Ubicación:

```text
app/prompts/email_prompts.py
```

Este archivo contendrá las instrucciones que orientarán a Gemini para redactar los correos.

**Actividad:**

1. Crear el archivo.
2. Definir una variable llamada `EMAIL_SYSTEM_PROMPT`.
3. Escribir instrucciones para que Gemini se comporte como un asistente de redacción empresarial.
4. Indicar que debe generar un asunto y un cuerpo de correo.

Puedes utilizar la siguiente estructura como punto de partida:

```python
EMAIL_SYSTEM_PROMPT = """
Eres un asistente especializado en redactar correos
electrónicos profesionales para el equipo de soporte
de Nexus SaaS.

Tu responsabilidad es generar correos claros,
cordiales y adecuados para la comunicación con clientes.

INSTRUCCIONES:

1. Utiliza un lenguaje profesional.
2. Adapta el tono a la solicitud recibida.
3. Organiza las ideas de manera clara.
4. No inventes información que no haya proporcionado
   el empleado.
5. No prometas fechas ni resultados no confirmados.
6. Genera un asunto y un cuerpo para el correo.
7. Mantén el contenido enfocado en la comunicación
   con clientes de Nexus SaaS.
"""
```

**Reto:** Agrega una instrucción que permita a Gemini adaptar el saludo y la despedida según el contexto del mensaje.

## Paso 2. Diseñar el prompt dinámico

Ahora necesitamos que el empleado pueda proporcionar información diferente para cada correo.

Debemos construir un prompt que incorpore los siguientes datos:

| Variable       | Descripción                                  |
| -------------- | -------------------------------------------- |
| `destinatario` | Nombre de la persona que recibirá el correo. |
| `motivo`       | Razón por la cual se redactará el mensaje.   |
| `detalles`     | Información adicional que debe incluirse.    |
| `tono`         | Estilo de comunicación solicitado.           |

**Actividad:**

Debajo de `EMAIL_SYSTEM_PROMPT`, crea una segunda variable llamada `EMAIL_USER_PROMPT`.

Utiliza esta estructura como referencia:

```python
EMAIL_USER_PROMPT = """
Redacta un correo electrónico considerando
la siguiente información:

Destinatario: {destinatario}

Motivo: {motivo}

Detalles: {detalles}

Tono: {tono}

El resultado debe contener:

- Asunto del correo.
- Cuerpo completo del mensaje.
"""
```

**Pregunta de reflexión:**

¿Por qué utilizamos `{destinatario}`, `{motivo}`, `{detalles}` y `{tono}` en lugar de escribir directamente los datos del cliente?

---

# Parte 2. Crear el servicio de generación de correos

## Paso 3. Crear `email_service.py`

Ubicación:

```text
app/services/email_service.py
```

Este servicio será responsable de comunicarse con Gemini.

Observa que ya tenemos un cliente configurado en:

```text
app/gemini_client.py
```

No necesitamos crear otro cliente de Gemini.

**Actividad:**

1. Importa el cliente existente.
2. Importa `types` desde `google.genai`.
3. Importa los dos prompts creados anteriormente.
4. Crea una función llamada `generar_email()`.

Estructura inicial:

```python
from google.genai import types

from app.gemini_client import client

from app.prompts.email_prompts import (
    EMAIL_SYSTEM_PROMPT,
    EMAIL_USER_PROMPT
)


def generar_email(destinatario, motivo, detalles, tono):

    # 1. Completar el prompt dinámico con los datos recibidos.


    # 2. Enviar la solicitud a Gemini utilizando
    #    el cliente existente.


    # 3. Recuperar el contenido generado por Gemini.


    # 4. Retornar el resultado.


```

**Reto:** Completa los cuatro puntos utilizando como referencia el servicio `chatbot_service.py`.

Ten presente que esta funcionalidad necesita enviar a Gemini tanto las instrucciones generales como la información específica del correo.

---

# Parte 3. Crear el modelo de entrada

## Paso 4. Crear `EmailRequest` en `main.py`

El endpoint necesitará recibir información desde Swagger o Postman.

Utilizaremos Pydantic para validar los datos.

**Actividad:**

En `main.py`, crea un modelo llamado `EmailRequest`.

Debe tener cuatro atributos:

- `destinatario`: texto obligatorio.
- `motivo`: texto obligatorio.
- `detalles`: texto obligatorio.
- `tono`: texto obligatorio.

Puedes utilizar como referencia el modelo `PreguntaRequest` que ya existe.

```python
class EmailRequest(BaseModel):

    # Agregar los atributos del correo.

    # Utilizar Field para establecer
    # restricciones de longitud.
```

**Reto:** Establece una longitud mínima y máxima para cada atributo utilizando `Field`.

---

# Parte 4. Crear el endpoint

## Paso 5. Importar el servicio

En `main.py`, importa la función `generar_email` desde:

```text
app/services/email_service.py
```

Recuerda que las rutas de los tres módulos estarán en el mismo archivo `main.py`.

## Paso 6. Crear el endpoint `POST /emails/generar`

El endpoint recibirá los datos del modelo `EmailRequest` y solicitará al servicio la generación del correo.

Estructura inicial:

```python
@app.post("/emails/generar")
def crear_email(datos: EmailRequest):

    try:

        # 1. Llamar a la función generar_email()
        #    enviando los cuatro atributos recibidos.


        # 2. Retornar un diccionario con:
        #    - destinatario
        #    - asunto o contenido generado
        #    - mensaje de confirmación


    except Exception as error:

        # 3. Manejar los posibles errores
        #    utilizando HTTPException.

        pass
```

**Reto:** Completa el endpoint y utiliza un código HTTP apropiado para los errores del servicio.

---

# Parte 5. Probar la funcionalidad

## Paso 7. Ejecutar la aplicación

Inicia FastAPI desde la terminal:

```powershell
uvicorn app.main:app --reload
```

Abre Swagger:

```text
http://127.0.0.1:8000/docs
```

## Paso 8. Probar el endpoint

Busca:

```text
POST /emails/generar
```

Utiliza el siguiente JSON:

```json
{
  "destinatario": "Carlos Rodríguez",
  "motivo": "Confirmación de recepción de solicitud",
  "detalles": "El equipo técnico está revisando un inconveniente con el acceso a su cuenta.",
  "tono": "Profesional y cordial"
}
```

**Verifica:**

- ¿Se genera un correo coherente con el motivo?
- ¿Se incluye el nombre del destinatario?
- ¿Se utiliza el tono solicitado?
- ¿Se conserva la información proporcionada?
- ¿Se evita inventar fechas o compromisos?

## Paso 9. Realizar una segunda prueba

Prueba ahora con una situación diferente:

```json
{
  "destinatario": "Laura Martínez",
  "motivo": "Notificación de finalización de mantenimiento",
  "detalles": "El mantenimiento programado de la plataforma ha finalizado y los servicios se encuentran disponibles.",
  "tono": "Cercano y profesional"
}
```

Compara los resultados de ambas solicitudes.

**Pregunta:** ¿Qué ventajas tiene utilizar un mismo servicio de generación de correos con diferentes datos de entrada?

---

# Parte 6. Reflexión y mejoras

## Paso 10. Analizar el funcionamiento

Responde las siguientes preguntas:

1. ¿Qué responsabilidad tiene `email_prompts.py`?
2. ¿Por qué la comunicación con Gemini se realiza desde `email_service.py`?
3. ¿Qué función cumple `EmailRequest`?
4. ¿Por qué el endpoint no contiene directamente toda la lógica de generación?
5. ¿Qué diferencia existe entre generar un correo y enviarlo?

## Desafíos adicionales

Estos desafíos no forman parte de la implementación obligatoria inicial:

- Agregar una variable para indicar el idioma del correo.
- Permitir generar correos de seguimiento.
- Crear diferentes plantillas de comunicación.
- Permitir solicitar una versión más corta del mensaje.
- Devolver el asunto y el cuerpo en campos independientes.
- Incorporar una interfaz para copiar el correo generado.

---

## Resultado esperado del módulo

Al finalizar, `SaaS Support AI` tendrá tres funcionalidades:

| Módulo                   | Funcionalidad                                 |
| ------------------------ | --------------------------------------------- |
| 1. Chatbot               | Responder consultas sobre Nexus SaaS.         |
| 2. Biblioteca de prompts | Consultar y generar prompts reutilizables.    |
| 3. Generador de correos  | Redactar correos profesionales utilizando IA. |

**Consideración:** La aplicación todavía no enviará correos electrónicos ni almacenará el historial de mensajes. Esas funcionalidades podrán incorporarse en futuras etapas del proyecto.
