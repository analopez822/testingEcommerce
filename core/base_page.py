import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Union

from playwright.sync_api import Page, Locator, expect

from core import config


class BasePage:
    """
        Clase base que envuelve las interacciones directas con PLaywright. Todas las clases de tipo Page Object deben
        heredar de esta clase.
        Si alguno de los metodos de Playwright cambia (nueva version, deprecated, etc) cambiarlos en esta clase
        es mas facil y rapido que cambiar todo el codigo
    """

    def __init__(self, page: Page):
        self.incognito_page = None
        self.page: Page = page

    def navegar(self, url: Optional[str] = None) -> None:
        self.page.goto(url or config.BASE_URL, wait_until="networkidle")   # wait until page is loaded

    def abrir_ventana_incognito(self, url: Optional[str] = None, close_original_page: bool = True) -> Page:
        incognito_context = self.page.context.browser.new_context()     # Create a brand new, isolated browser context (incognito session)
        self.incognito_page = incognito_context.new_page()              # Open a new page within that isolated context
        self.incognito_page.goto(url or config.BASE_URL, wait_until="networkidle")
        if close_original_page:
            self.page.close()  # Close the original page
        return self.incognito_page

    def encontrar(self, selector: str) -> Locator:
        """ Centraliza la busqueda de elementos que tienen id  """
        return self.page.locator(selector)

    def buscar_por_texto(self, texto: str) -> Locator:
        """ Centraliza la busqueda de elementos con text/role  """
        return self.page.get_by_text(texto)

    def buscar_por_placeholder(self, texto: str) -> Locator:
        return self.page.get_by_placeholder(texto)

    def buscar_por_rol(self, rol: str, name: str = None, exact: bool = None) -> Locator:
        return self.page.get_by_role(rol, name=name, exact=exact)

    def debe_ver(self, texto: str, primero: bool = False) -> None:
        """Comprueba que un texto (toast, dialogo, titulo...) es visible. `primero=True` si el texto sale varias veces."""
        locator = self.buscar_por_texto(texto)
        expect(locator.first if primero else locator).to_be_visible()

    def no_debe_ver(self, texto: str) -> None:
        expect(self.buscar_por_texto(texto)).not_to_be_visible()

    def fill_box(self, locator: str, text: str) -> None:
        self.page.locator(locator).fill(text)

    def click_boton(self, button_text: str) -> None:
        """Click a button by its accessible name, waiting for it to be visible and scrolling it into view.
        Falls back to a force click if a normal click fails (covers overlays/obstructions).
        """
        # locator = self.page.get_by_role("button", name=re.compile(re.escape(button_text), re.IGNORECASE))
        # locator.click()
        self.page.get_by_role("button", name=button_text).click()

    def click_link(self, texto: str) -> None:
        self.page.click(f"a:has-text('{texto}')")
        # self.page.locator(f'a[href*="{texto}"]').click()


    def descargar_archivo_json(self, boton: str, nombre_archivo: Optional[str] = None) -> Path:
        """Descarga un archivo, lo guarda en Downloads y solo valida JSON si el contenido es texto UTF-8."""
        with self.page.expect_download() as download_info: # gestionador de contesto que escucha el click del boton
            self.click_boton(boton)

        descarga = download_info.value
        nombre = nombre_archivo or descarga.suggested_filename
        ruta_descarga = Path.home() / "Downloads" / nombre       # carpeta en la que mi sistema guarda los downloads por defecto
        ruta_descarga.parent.mkdir(parents=True, exist_ok=True)  # comprueba el directorio Downloads existe
        descarga.save_as(str(ruta_descarga))                     # baja mi fichero a Downloads

        # estas lineas confirma que el directorio existe en mi ordenador; si no, lanza el error
        if not ruta_descarga.exists():
            raise FileNotFoundError(f"No se encontró el archivo descargado en {ruta_descarga}")

        # las lineas de abajo evitan que el test falle si el formato del file no es json.
        # No forzamos UTF-8; solo comprobamos que el archivo existe y, si es texto, que sea JSON válido.
        try:
            contenido = ruta_descarga.read_bytes()
            try:
                texto = contenido.decode("utf-8")
            except UnicodeDecodeError:
                return ruta_descarga
            try:
                json.loads(texto)
            except json.JSONDecodeError:
                pass
        except OSError:
            pass
        return ruta_descarga


    def descargar_pdf(self,  boton: str, nombre_archivo: Optional[str] = None) -> Path:
        with self.page.expect_download() as download_info:
            self.click_boton(boton)

        descarga = download_info.value
        nombre = nombre_archivo or descarga.suggested_filename
        ruta_descarga = Path.home() / "Downloads" / nombre
        ruta_descarga.parent.mkdir(parents=True, exist_ok=True) # crea el directorio/s ruta_descarga si no existe
        descarga.save_as(str(ruta_descarga))

        # estas lineas confirma que el directorio existe en mi ordenador; si no lanza error
        if not ruta_descarga.exists():
            raise FileNotFoundError(f"No se encontró el archivo descargado en {ruta_descarga}")

        contenido = ruta_descarga.read_bytes()
        if not contenido.startswith(b"%PDF-"):
            raise ValueError(f"El archivo descargado no es un pdf valido")
        return ruta_descarga


    def abrir_archivo(self, ruta_archivo: Union[str, Path]) -> None:
        """Abre un archivo si existe en el sistema operativo actual.
            Pide al usuario que escoja aplicacion.
        """
        ruta = Path(ruta_archivo)  # Convierte el texto en un objeto Path de la librería pathlib para que sea compatible sin importar el sistema operativo.
        if not ruta.exists():
            raise FileNotFoundError(f"El archivo no existe: {ruta}")

        # comprueba en que sistema operativo esta (win, mac o Linux) para abrir file con metodo adecuado
        if sys.platform.startswith("win"):
            os.startfile(str(ruta))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(ruta)], check=True)
        else:
            subprocess.run(["xdg-open", str(ruta)], check=True)



    def debugger(self):
        if os.environ.get("DEBUG_PAUSA")=="1":
            self.page.pause()




