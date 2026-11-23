from playwright.sync_api import Page, expect

from components.lista_tarjetas import ListaTarjetas, SELECTOR_REJILLA
from core.base_page import BasePage
from core.vocabulario import Boton, Panel


class DireccionesSeccion(BasePage):
    """Mi cuenta > Direcciones: lista de direcciones guardadas, borrar y editar."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.lista = ListaTarjetas(page, SELECTOR_REJILLA)

        self._direcciones_header: str = "Las que te proponemos al finalizar la compra."
        self._dialogo_eliminar: str = "Eliminar dirección"
        self._confirmacion_direccion_eliminada: str = "Dirección eliminada"
        self._boton_editar: str = "Editar"
        self._dialogo_editar: str = "Solo enviamos a países de la Unión Europea."

    def abrir(self) -> None:
        self.click_link(Panel.DIRECCIONES)
        self.debe_ver(self._direcciones_header)

    def describir(self) -> None:
        self.lista.describir("direcciones", "Direccion")

    def eliminar(self, indice: int) -> None:
        """Borra la direccion que ocupa la posicion `indice` (0 = primera) y comprueba que desaparece."""
        direccion = self.lista.items.nth(indice)
        self.buscar_por_texto(Boton.ELIMINAR).nth(indice).click()
        self.debe_ver(self._dialogo_eliminar)
        self.click_boton(Boton.ELIMINAR)
        self.debe_ver(self._confirmacion_direccion_eliminada)
        expect(direccion).not_to_be_visible()

    def abrir_edicion(self, indice: int = 0) -> None:
        self.buscar_por_texto(self._boton_editar).nth(indice).click()
        self.debe_ver(self._dialogo_editar)
