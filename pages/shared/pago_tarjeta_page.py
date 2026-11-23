from core.base_page import BasePage
from datos.prueba import Tarjeta
from playwright.sync_api import Page, FrameLocator, Locator, expect

class PagoTarjetaPage(BasePage):
    """
        Clase con los locators y metodos de Pago con Tarjeta (formulario seguro dentro de un iframe)
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina pago con tarjeta
        self._formulario_pago_tarjeta: str = "Pago seguro"
        self._iframe: str = "iframe[title='Campo de entrada seguro para el pago']"
        self._boton_pagar: str = "Pagar "
        self._pago_confirmado: str = "Pago confirmado"

    @property
    def iframe(self) -> FrameLocator:
        return self.page.frame_locator(self._iframe)

    def debe_mostrar_formulario(self) -> None:
        self.debe_ver(self._formulario_pago_tarjeta, primero=True)

    def boton_pagar(self, indice: int) -> Locator:
        """El texto 'Pagar ' sale varias veces en la pagina; el indice (2 tarjeta, 4 Klarna/PayPal) elige el correcto."""
        return self.buscar_por_texto(self._boton_pagar).nth(indice)

    def elegir_pestana(self, nombre: str) -> None:
        """Cambia de metodo de pago dentro del iframe: 'klarna', 'paypal'..."""
        self.iframe.locator(f"button[id='{nombre}-tab']").click()

    def pagar_con_tarjeta(self, t: Tarjeta, indice_boton_pagar: int = 2) -> None:
        boton_pagar = self.boton_pagar(indice_boton_pagar)
        self.iframe.locator("input[id='payment-numberInput']").fill(t.numero)
        self.iframe.locator("input[id='payment-expiryInput']").fill(t.caducidad)
        self.iframe.locator("input[id='payment-cvcInput']").fill(t.cvc)
        self.iframe.locator("select[id='payment-countryInput']").select_option(t.pais)
        self.iframe.locator("input[id='payment-linkEmailInput']").fill(t.email)
        self.iframe.locator("input[id='payment-linkMobilePhoneInput']").fill(t.movil)
        self.iframe.locator("input[id='payment-linkLegalNameInput']").fill(t.nombre)
        boton_pagar.scroll_into_view_if_needed()
        expect(boton_pagar).to_be_visible()
        boton_pagar.click()
