# tests/api/test_api.py
#
# Pruebas de API usando JSONPlaceholder, una API pública gratuita de tipo REST.
# Es ideal para demos y aprendizaje porque no requiere autenticación ni API key.
#
# Base URL: https://jsonplaceholder.typicode.com
# Guía:     https://jsonplaceholder.typicode.com/guide/

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ---------------------------------------------------------------------------
# Test 1 – GET exitoso a la lista de posts
# ---------------------------------------------------------------------------
# Escenario:
# Consumimos el endpoint /posts para obtener la lista completa de publicaciones.
# Este tipo de prueba sirve para validar lo más básico de una API:
# 1. que el endpoint responda correctamente
# 2. que el status code sea el esperado
# 3. que la estructura de la respuesta tenga la forma correcta

def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")

    # Validamos que la API haya respondido con HTTP 200 (OK)
    # Esto significa que la solicitud fue procesada exitosamente.
    assert response.status_code == 200, (
        f"Se esperaba status 200, pero se obtuvo {response.status_code}"
    )

    # Convertimos el body JSON a una lista de Python
    posts = response.json()

    # Validamos que la respuesta sea una lista
    # y que contenga exactamente 100 registros.
    assert isinstance(posts, list), "El body de la respuesta debe ser una lista JSON"
    assert len(posts) == 100, f"Se esperaban 100 posts, pero se obtuvieron {len(posts)}"

    # Validación de estructura:
    # revisamos que cada post tenga los campos mínimos esperados.
    # Aquí no validamos valores exactos, sino que la forma de los datos sea correcta.
    for post in posts:
        assert "id" in post, "Cada post debe incluir el campo 'id'"
        assert "title" in post, "Cada post debe incluir el campo 'title'"
        assert "body" in post, "Cada post debe incluir el campo 'body'"
        assert "userId" in post, "Cada post debe incluir el campo 'userId'"


# ---------------------------------------------------------------------------
# Test 2 – validación de un recurso específico (GET /posts/1)
# ---------------------------------------------------------------------------
# Escenario:
# Consumimos un recurso puntual, en este caso el post con id = 1.
# Este patrón sirve cuando queremos validar:
# 1. el status code
# 2. la presencia de los campos esperados
# 3. algunos valores concretos de un registro conocido

def test_get_single_post():
    post_id = 1
    response = requests.get(f"{BASE_URL}/posts/{post_id}")

    # Como el recurso existe, esperamos una respuesta exitosa.
    assert response.status_code == 200, (
        f"Se esperaba status 200, pero se obtuvo {response.status_code}"
    )

    # Convertimos el body JSON a un diccionario de Python
    post = response.json()

    # Validamos que el objeto incluya todas las llaves necesarias
    assert "id" in post, "La respuesta debe incluir el campo 'id'"
    assert "userId" in post, "La respuesta debe incluir el campo 'userId'"
    assert "title" in post, "La respuesta debe incluir el campo 'title'"
    assert "body" in post, "La respuesta debe incluir el campo 'body'"

    # Validamos algunos valores esperados del recurso consultado.
    # Como este endpoint público es determinístico, podemos verificar datos puntuales.
    assert post["id"] == post_id, (
        f"Se esperaba post id {post_id}, pero se obtuvo {post['id']}"
    )
    assert post["userId"] == 1, (
        f"Se esperaba userId 1, pero se obtuvo {post['userId']}"
    )

    # Validamos que el título tenga contenido y no venga vacío.
    assert isinstance(post["title"], str) and len(post["title"]) > 0, (
        "El título del post debe ser un string no vacío"
    )
