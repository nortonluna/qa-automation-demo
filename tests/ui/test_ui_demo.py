# tests/ui/test_ui_demo.py
#
# Pruebas automatizadas de UI para la página de login de Practice Test Automation.
# Usamos Selenium para controlar un navegador real y validar el comportamiento esperado.
#
# Página bajo prueba: https://practicetestautomation.com/practice-test-login/
# Credenciales válidas: username=student  password=Password123

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://practicetestautomation.com/practice-test-login/"
EXCEPTIONS_URL = "https://practicetestautomation.com/practice-test-exceptions/"


# ---------------------------------------------------------------------------
# Fixture: browser
# ---------------------------------------------------------------------------
# Una fixture de pytest sirve para preparar y limpiar recursos reutilizables.
# En este caso:
# 1. Antes de cada prueba, abre Chrome con la configuración indicada.
# 2. Le entrega ese navegador al test.
# 3. Cuando el test termina, cierra el navegador automáticamente.
#
# "yield" divide la fixture en dos partes:
# - Antes de yield: preparación (setup)
# - Después de yield: limpieza (teardown)

@pytest.fixture
def browser():
    options = Options()

    # Si el test corre en CI/CD, usamos modo headless
    # para que el navegador se ejecute sin ventana visible.
    if os.getenv("CI") == "true":
        options.add_argument("--headless")

    # Estas opciones ayudan a que Chrome corra mejor en ambientes de CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Crea una instancia real del navegador Chrome
    driver = webdriver.Chrome(options=options)

    # Espera implícita:
    # Selenium intentará encontrar elementos por hasta 5 segundos
    # antes de lanzar error.
    driver.implicitly_wait(5)

    # Entrega el navegador al test
    yield driver

    # Cierra el navegador al finalizar el test, incluso si falla
    driver.quit()


# ---------------------------------------------------------------------------
# Helpers: abrir paginas del sitio
# ---------------------------------------------------------------------------
# Esta función existe para no repetir driver.get(...) en varios tests.
# Ayuda a mantener el código más limpio y legible.

def open_login_page(driver):
    driver.get(LOGIN_URL)

def open_exceptions_page(driver):
    driver.get(EXCEPTIONS_URL)


# ---------------------------------------------------------------------------
# Test 1 – login válido
# ---------------------------------------------------------------------------
# Escenario:
# El usuario ingresa credenciales correctas
# y se espera que llegue a la página de login exitoso.

def test_valid_login(browser):
    # Abrimos la página de login
    open_login_page(browser)

    # Buscamos los campos username y password por ID
    # y escribimos credenciales válidas
    browser.find_element(By.ID, "username").send_keys("student")
    browser.find_element(By.ID, "password").send_keys("Password123")

    # Hacemos click en el botón Submit
    browser.find_element(By.ID, "submit").click()

    # Espera explícita:
    # esperamos hasta 10 segundos a que la URL cambie
    # y contenga "logged-in-successfully"
    WebDriverWait(browser, 10).until(
        EC.url_contains("logged-in-successfully")
    )

    # Validación 1:
    # confirmamos que la URL actual sí corresponde a la página de éxito
    assert "logged-in-successfully" in browser.current_url, (
        f"Expected URL to contain 'logged-in-successfully', got: {browser.current_url}"
    )

    # Validación 2:
    # confirmamos que el cuerpo de la página contiene un mensaje de éxito
    page_text = browser.find_element(By.TAG_NAME, "body").text
    assert "Congratulations" in page_text or "successfully logged in" in page_text.lower(), (
        "Success message not found on page after valid login"
    )

    # Pausa breve para que el flujo se vea en la demo local
    time.sleep(4)


# ---------------------------------------------------------------------------
# Test 2 – login inválido por username incorrecto
# ---------------------------------------------------------------------------
# Escenario:
# El usuario ingresa un username incorrecto con password válida
# y se espera un mensaje de error.

def test_invalid_login_wrong_username(browser):
    # Abrimos la página de login
    open_login_page(browser)

    # Escribimos un username inválido intencionalmente
    browser.find_element(By.ID, "username").send_keys("wronguser")
    browser.find_element(By.ID, "password").send_keys("Password123")

    # Hacemos click en Submit
    browser.find_element(By.ID, "submit").click()

    # Espera explícita:
    # esperamos hasta que el mensaje de error aparezca visible en pantalla
    error_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "error"))
    )

    # Validación:
    # confirmamos que el texto del error sea el esperado
    assert "Your username is invalid!" in error_element.text, (
        f"Expected 'Your username is invalid!' in error text, got: {error_element.text}"
    )

    # Pausa breve para que el flujo se vea en la demo local
    time.sleep(4)



# ---------------------------------------------------------------------------
# Test 3 – aparición de Row 2 usando espera explícita
# ---------------------------------------------------------------------------
# Escenario:
# Al hacer click en el botón Add, la fila 2 no aparece inmediatamente.
# Por eso usamos una espera explícita para darle tiempo a la página
# de actualizar el DOM antes de validar que el input de Row 2 ya es visible.

def test_row_2_appears_after_clicking_add(browser):
    # Abrimos la página de excepciones
    open_exceptions_page(browser)

    # Hacemos click en el botón Add
    browser.find_element(By.ID, "add_btn").click()

    # Esperamos hasta 10 segundos a que el input de Row 2 sea visible
    row_2_input = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#row2 input"))
    )

    # Validamos que el input de Row 2 sí esté visible en pantalla
    assert row_2_input.is_displayed(), "El input de Row 2 no se mostró después de hacer click en Add"

    # Pausa breve para que el flujo se vea
    time.sleep(4)

