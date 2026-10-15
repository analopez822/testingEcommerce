from core.base_page import BasePage
from playwright.sync_api import Page

class FinalizarCompraPage(BasePage):
    """
        Clase con los locators y metodos de Finalizar Compra
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina finalizar compra
        self._texto_finalizar_compra: str = "Finalizar compra"
        self._nombre: str = 'input[name="fullName"]'      # input data-slot="input" name=fullName   'fullName'
        # self._nombre: str = 'label[name="Nombre y apellidos"]'      # label data-slot="field-label"  "Nombre y apellidos"
        self._direccion: str = 'input[name="street"]'
        self._codigo_postal: str = 'input[name="postalCode"]'
        self._ciudad: str = 'input[name="city"]'
        # self._pais: str =  this is disabled!!
        self._provincia: str = 'input[name="province"]'
        self._telefono: str = 'input[name="phone"]'
        self._notas_entrega: str = 'textarea[name="notes"]'
        self._guardar_direccion_boton: str = "Guardar dirección"
        self._confirmar_pedido_boton: str = "Confirmar pedido"
        self._cancelar_compra_boton: str = "Cancelar compra"
        self._direccion_guardada: str = "Dirección guardada"
        self._tarjeta_boton: str = "Tarjeta, Apple Pay o Google Pay"

        # locators pagina confirmacion de pedido

        # locators pagina cancelar compra
        self._cancelar_dialogo: str = "¿Cancelar la compra?"
        self._cancelar: str = "Cancelar"
        self._compra_cancelada: str = "Compra cancelada"
