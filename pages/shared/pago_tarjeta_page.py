from core.base_page import BasePage
from playwright.sync_api import Page

class PagoTarjetaPage(BasePage):
    """
        Clase con los locators y metodos de Pago con Tarjeta
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina pago con tarjeta
        self._formulario_pago_tarjeta: str = "Pago seguro"
        self._numero_tarjeta: str = 'input[aria-label="Número de tarjeta"]'
        self._numero_tarjeta_robusto: str = "input[autocomplete='cc-number'], input[aria-label='Card number'], input[aria-label='Número de tarjeta']"
        self._fecha_caducidad: str = "input[placeholder='MM / AA']"   #  "#payment-expiryInput"
        self._codigo_seguridad: str = "#payment-cvcInput"
        self._pais: str = "#payment-countryInput"
        self._email: str = "#payment-linkEmailInput"
        self._movil: str = "#payment-linkMobilePhoneInput"
        self._nombre: str = "#payment-linkLegalNameInput"
        self._boton_pagar: str = "Pagar "

    def fill_box(self, locator: str, text: str) -> None:
        if any(token in locator for token in ("Número de tarjeta", "Card number", "cc-number", "cardnumber")):
            selector = self._numero_tarjeta_robusto
            field = self.page.locator(selector)
            if field.count() == 0:
                field = self.page.frame_locator("iframe[title*='Secure card payment input frame']").locator(selector)
            field.first.fill(text)
            return
        super().fill_box(locator, text)



