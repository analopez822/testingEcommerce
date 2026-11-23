from playwright.sync_api import Page, Locator, expect

from core.base_page import BasePage
from core.vocabulario import Panel

SELECTOR_MENSAJES = "ul[class='flex flex-col gap-3'] > li"


class ChatDialogo(BasePage):
    """
    Chat con la tienda. Sirve igual para el cliente (abre el chat) que para el admin
    (elige la conversacion de un cliente y escribe).
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self._boton_abrir: str = "Abrir el chat"
        self._titulo: str = "Chat con la tienda"
        self._caja_mensaje: str = "Escribe tu mensaje"            # placeholder
        self._boton_enviar: str = "Enviar"
        self._boton_conversacion: str = "button[class*='flex flex-col gap-0.5']"   # una conversacion por cliente (vista admin)

    def ir_a_conversaciones(self) -> None:
        """Vista admin: entra en 'Chat' desde el panel izquierdo."""
        self.click_link(Panel.CHAT)

    def abrir(self) -> None:
        self.click_boton(self._boton_abrir)
        self.debe_ver(self._titulo)

    def enviar(self, mensaje: str) -> None:
        self.buscar_por_placeholder(self._caja_mensaje).fill(mensaje)
        self.click_boton(self._boton_enviar)

    def debe_mostrar(self, mensaje: str) -> None:
        self.debe_ver(mensaje, primero=True)

    def ultimo_mensaje(self) -> Locator:
        return self.page.locator(SELECTOR_MENSAJES).last

    def abrir_conversacion_con(self, nombre: str) -> None:
        """Vista admin: abre la conversacion del cliente cuyo nombre contiene `nombre`."""
        conversacion = self.encontrar(self._boton_conversacion).filter(has_text=nombre).first
        expect(conversacion).to_be_visible()
        conversacion.click()
