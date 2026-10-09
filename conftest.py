import pytest, os
from typing import Generator
from slugify import slugify
from playwright.sync_api import Page

from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Intercepta el resultado de cada prueba.
    Si la prueba falla, busca la captura de pantalla generada por Playwright
    y la incrusta en el reporte HTML.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        # Playwright guarda las capturas usando un slug del nombre del test
        nombre_test_limpio = slugify(item.nodeid)
        ruta_captura = f"test-results/{nombre_test_limpio}/test-failed-1.png"

        if os.path.exists(ruta_captura):
            # Codificamos la imagen en base64 para que el HTML siga siendo self-contained
            import base64
            with open(ruta_captura, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                html_img = f'<div><img src="data:image/png;base64,{encoded_string}" alt="screenshot" style="width:600px;height:auto;" onclick="window.open(this.src)" align="right"/></div>'
                extra.append(pytest_html.extras.html(html_img))

        report.extra = extra


# Configuraciones globales que aplicarán a todas las pruebas
@pytest.fixture(scope="session", autouse=True)
def configuracion_global():
    """Se ejecuta una sola vez antes de toda la suite."""
    print("\n[INFO] Inicializando entorno de pruebas automatizadas...")
    yield
    print("\n[INFO] Finalizando ejecución y limpiando recursos...")


@pytest.fixture(scope="function")
def app_login(page: Page) -> Generator[LoginPage, None, None]:
    """Inyecta el contexto de las pruebas de la app de login"""
    login_page = LoginPage(page)
    yield login_page

@pytest.fixture(scope="function")
def app_navegacion(page: Page) -> Generator[NavegacionPage, None, None]:
    """Inyecta el contexto de las pruebas de la app de navegación"""
    navegacion_page = NavegacionPage(page)
    yield navegacion_page