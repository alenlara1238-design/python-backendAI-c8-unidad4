import pytest


def crear_evento(
    client,
    titulo="Taller",
    descripcion="Introducción",
    capacidad=20,
):
    response = client.post(
        "/eventos/",
        json={
            "titulo": titulo,
            "descripcion": descripcion,
            "capacidad": capacidad,
        },
    )
    assert response.status_code == 201
    return response.json()


def test_listar_eventos_vacio(client):
    response = client.get("/eventos/")

    assert response.status_code == 200
    assert response.json() == []


def test_listar_eventos_devuelve_los_creados(client):
    primero = crear_evento(client, titulo="Taller", capacidad=10)
    segundo = crear_evento(client, titulo="Conferencia", capacidad=30)

    response = client.get("/eventos/")

    assert response.status_code == 200
    assert response.json() == [primero, segundo]


def test_obtener_evento_por_id(client):
    creado = crear_evento(client)

    response = client.get(f"/eventos/{creado['id']}")

    assert response.status_code == 200
    assert response.json() == creado


def test_crear_evento(client):
    response = client.post(
        "/eventos/",
        json={
            "titulo": "Taller",
            "descripcion": "Introducción",
            "capacidad": 20,
        },
    )

    assert response.status_code == 201
    cuerpo = response.json()
    assert isinstance(cuerpo["id"], int)
    assert cuerpo["titulo"] == "Taller"
    assert cuerpo["descripcion"] == "Introducción"
    assert cuerpo["capacidad"] == 20


def test_crear_evento_recorta_titulo(client):
    response = client.post(
        "/eventos/",
        json={
            "titulo": "  Taller  ",
            "descripcion": "Introducción",
            "capacidad": 20,
        },
    )

    assert response.status_code == 201
    assert response.json()["titulo"] == "Taller"


def test_crear_evento_sin_descripcion(client):
    response = client.post(
        "/eventos/",
        json={
            "titulo": "Taller",
            "capacidad": 20,
        },
    )

    assert response.status_code == 201
    assert response.json()["descripcion"] is None


def test_actualizar_evento(client):
    creado = crear_evento(client)

    response = client.put(
        f"/eventos/{creado['id']}",
        json={
            "titulo": "Taller avanzado",
            "descripcion": "Segunda sesión",
            "capacidad": 40,
        },
    )

    assert response.status_code == 200
    actualizado = response.json()
    assert actualizado["id"] == creado["id"]
    assert actualizado["titulo"] == "Taller avanzado"
    assert actualizado["descripcion"] == "Segunda sesión"
    assert actualizado["capacidad"] == 40

    consulta = client.get(f"/eventos/{creado['id']}")
    assert consulta.status_code == 200
    assert consulta.json() == actualizado


def test_actualizar_evento_recorta_titulo(client):
    creado = crear_evento(client)

    response = client.put(
        f"/eventos/{creado['id']}",
        json={
            "titulo": "  Taller avanzado  ",
            "descripcion": "Segunda sesión",
            "capacidad": 40,
        },
    )

    assert response.status_code == 200
    assert response.json()["titulo"] == "Taller avanzado"


def test_actualizar_evento_sin_descripcion_la_deja_en_null(client):
    creado = crear_evento(client, descripcion="Introducción")

    response = client.put(
        f"/eventos/{creado['id']}",
        json={
            "titulo": "Taller",
            "capacidad": 20,
        },
    )

    assert response.status_code == 200
    assert response.json()["descripcion"] is None


def test_actualizar_un_evento_no_altera_otro(client):
    primero = crear_evento(client, titulo="Taller", descripcion="Uno", capacidad=10)
    segundo = crear_evento(client, titulo="Conferencia", descripcion="Dos", capacidad=30)

    response = client.put(
        f"/eventos/{primero['id']}",
        json={
            "titulo": "Taller nuevo",
            "descripcion": "Actualizado",
            "capacidad": 15,
        },
    )

    assert response.status_code == 200

    consulta = client.get(f"/eventos/{segundo['id']}")
    assert consulta.status_code == 200
    assert consulta.json() == segundo


def test_obtener_evento_inexistente(client):
    response = client.get("/eventos/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Evento no encontrado"


def test_actualizar_evento_inexistente(client):
    response = client.put(
        "/eventos/999",
        json={
            "titulo": "Taller",
            "descripcion": "Introducción",
            "capacidad": 20,
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Evento no encontrado"


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"titulo": "", "capacidad": 20},
        {"titulo": "Taller", "capacidad": 0},
    ],
)
def test_actualizar_inexistente_prioriza_404(client, cuerpo):
    response = client.put("/eventos/999", json=cuerpo)

    assert response.status_code == 404
    assert response.json()["detail"] == "Evento no encontrado"


@pytest.mark.parametrize("titulo", ["", "   "])
def test_crear_evento_rechaza_titulo_vacio(client, titulo):
    response = client.post(
        "/eventos/",
        json={
            "titulo": titulo,
            "descripcion": "Introducción",
            "capacidad": 20,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El título del evento es obligatorio"


@pytest.mark.parametrize("titulo", ["", "   "])
def test_actualizar_evento_rechaza_titulo_vacio(client, titulo):
    creado = crear_evento(client)

    response = client.put(
        f"/eventos/{creado['id']}",
        json={
            "titulo": titulo,
            "descripcion": "Otra",
            "capacidad": 50,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El título del evento es obligatorio"


@pytest.mark.parametrize("capacidad", [0, -1])
def test_crear_evento_rechaza_capacidad_invalida(client, capacidad):
    response = client.post(
        "/eventos/",
        json={
            "titulo": "Taller",
            "descripcion": "Introducción",
            "capacidad": capacidad,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "La capacidad debe ser mayor que cero"


@pytest.mark.parametrize("capacidad", [0, -1])
def test_actualizar_evento_rechaza_capacidad_invalida(client, capacidad):
    creado = crear_evento(client)

    response = client.put(
        f"/eventos/{creado['id']}",
        json={
            "titulo": "Taller",
            "descripcion": "Introducción",
            "capacidad": capacidad,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "La capacidad debe ser mayor que cero"


def test_actualizar_con_error_400_no_modifica_el_evento(client):
    creado = crear_evento(client)

    response = client.put(
        f"/eventos/{creado['id']}",
        json={
            "titulo": "   ",
            "descripcion": "Cambiada",
            "capacidad": 99,
        },
    )

    assert response.status_code == 400

    consulta = client.get(f"/eventos/{creado['id']}")
    assert consulta.status_code == 200
    assert consulta.json() == creado


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"descripcion": "Introducción", "capacidad": 20},
        {"titulo": "Taller", "descripcion": "Introducción"},
        {"titulo": "Taller", "descripcion": "Introducción", "capacidad": "muchos"},
        {"titulo": ["Taller"], "descripcion": "Introducción", "capacidad": 20},
    ],
)
def test_crear_evento_rechaza_cuerpo_invalido(client, cuerpo):
    response = client.post("/eventos/", json=cuerpo)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "cuerpo",
    [
        {"descripcion": "Introducción", "capacidad": 20},
        {"titulo": "Taller", "descripcion": "Introducción"},
        {"titulo": "Taller", "descripcion": "Introducción", "capacidad": "muchos"},
        {"titulo": ["Taller"], "descripcion": "Introducción", "capacidad": 20},
    ],
)
def test_actualizar_evento_rechaza_cuerpo_invalido(client, cuerpo):
    creado = crear_evento(client)

    response = client.put(f"/eventos/{creado['id']}", json=cuerpo)

    assert response.status_code == 422


def test_obtener_evento_con_id_no_entero(client):
    response = client.get("/eventos/abc")

    assert response.status_code == 422


def test_actualizar_evento_con_id_no_entero(client):
    response = client.put(
        "/eventos/abc",
        json={
            "titulo": "Taller",
            "descripcion": "Introducción",
            "capacidad": 20,
        },
    )

    assert response.status_code == 422


def test_actualizar_con_error_422_no_modifica_el_evento(client):
    creado = crear_evento(client)

    response = client.put(
        f"/eventos/{creado['id']}",
        json={"capacidad": "muchos"},
    )

    assert response.status_code == 422

    consulta = client.get(f"/eventos/{creado['id']}")
    assert consulta.status_code == 200
    assert consulta.json() == creado
