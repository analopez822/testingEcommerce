from core.base_page import BasePage
from playwright.sync_api import Page

class MiCuentaPage(BasePage):
    """
        Clase con los locators y metodos de Mi Cuenta
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators Mi Cuenta
        self._datos_personales: str = "Datos personales"
        self._boton_guardar_cambios: str = "Guardar cambios"
        self._correo: str = "Correo electrónico"
        self._boton_correo: str = "Cambiar email"
        self._descargar_datos: str = "Descargar mis datos"
        self._boton_descargar_datos: str = "Descargar JSON"
        self._eliminar_cuenta: str = "Eliminar mi cuenta"
        self._boton_solicitar_baja: str = "Solicitar la baja"

        # locators panel izquierdo
        self._mis_datos: str = "Mis datos"
        self._texto_mis_datos: str = "Tu información personal y cómo entras en la tienda."
        self._mis_pedidos: str = "Mis pedidos"
        self._direcciones: str = "Direcciones"
        self._metodos_pago: str = 'Métodos de pago'
        self._devoluciones: str = 'Devoluciones'
        self._seguridad: str = 'Seguridad'
        self._soporte: str = 'Soporte'

