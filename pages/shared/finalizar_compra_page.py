from core.base_page import BasePage
from core.vocabulario import Boton, Campo
from datos.prueba import Direccion
from playwright.sync_api import Page

class FinalizarCompraPage(BasePage):
    """
        Clase con los locators y metodos de Finalizar Compra
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina finalizar compra
        self._texto_finalizar_compra: str = Boton.FINALIZAR_COMPRA
        self._nombre: str = 'input[name="fullName"]'      # input data-slot="input" name=fullName   'fullName'
        self._direccion: str = 'input[id="street"]'
        self._codigo_postal: str = 'input[name="postalCode"]'
        self._ciudad: str = "input[placeholder='Buscar ciudad']"   # CAMBIO!  "Elige tu ciudad"   #'input[name="city"]'
        # self._pais: str =  this is disabled!!
        self._provincia: str = 'input[name="province"]'
        self._telefono: str = Campo.TELEFONO
        self._notas_entrega: str = 'textarea[name="notes"]'
        self._guardar_direccion_boton: str = "Guardar dirección"
        self._otras_direcciones: str = "Tus direcciones"
        self._boton_otra_direccion: str = "Usar otra dirección"
        self._confirmar_pedido_boton: str = "Confirmar pedido"
        self._cancelar_compra_boton: str = "Cancelar compra"
        self._direccion_guardada: str = "Dirección guardada"
        self._direccion_actualizada: str = "Dirección actualizada"
        self._tarjeta_boton: str = Boton.PAGAR_CON_TARJETA
        self._pedido_creado: str = " creado"

        # locators pagina checkboxes
        self._condiciones: str = "#accept-terms"
        self._desistimiento: str = "#accept-withdrawal"

        # locators pagina cancelar compra
        self._cancelar_dialogo: str = "¿Cancelar la compra?"
        self._compra_cancelada: str = "Compra cancelada"

    def debe_mostrar_pagina(self) -> None:
        self.debe_ver(self._texto_finalizar_compra)

    def rellenar_direccion(self, d: Direccion) -> None:
        """Rellena el formulario de direccion, lo guarda y comprueba el toast 'Dirección guardada'."""
        self.fill_box(self._nombre, d.nombre)
        self.page.locator("button[role='combobox']").nth(1).click()
        self.fill_box(self._ciudad, d.ciudad)
        self.page.locator("ul[class='max-h-64 overflow-y-auto p-1']").locator("button").first.click()
        self.fill_box(self._direccion, d.calle)
        self.fill_box(self._codigo_postal, d.codigo_postal)
        self.fill_box(self._provincia, d.provincia)
        self.fill_box(self._telefono, d.telefono)
        self.fill_box(self._notas_entrega, d.notas)
        self.click_boton(self._guardar_direccion_boton)
        self.debe_ver(self._direccion_guardada)

    def cargar_direccion(self, d: Direccion) -> None:
        """Si el usuario ya tiene direcciones guardadas pulsa 'Usar otra dirección'; despues rellena el formulario."""
        if self.buscar_por_texto(self._otras_direcciones).count() > 0:
            self.buscar_por_rol("button", self._boton_otra_direccion).click()
        self.rellenar_direccion(d)

    def editar_contacto(self, d: Direccion) -> None:
        """Dialogo de editar direccion: cambia provincia, telefono y notas, guarda y comprueba el toast."""
        self.fill_box(self._provincia, d.provincia)
        self.fill_box(self._telefono, d.telefono)
        self.fill_box(self._notas_entrega, d.notas)
        self.click_boton(self._guardar_direccion_boton)
        self.debe_ver(self._direccion_actualizada)

    def elegir_pago_con_tarjeta(self) -> None:
        self.buscar_por_texto(self._tarjeta_boton).click()

    def aceptar_condiciones(self) -> None:
        self.encontrar(self._condiciones).check()
        self.encontrar(self._desistimiento).check()

    def confirmar_pedido(self) -> None:
        self.click_boton(self._confirmar_pedido_boton)

    def cancelar_compra(self) -> None:
        """Pulsa 'Cancelar compra', confirma en el dialogo y comprueba el toast 'Compra cancelada'."""
        self.click_boton(self._cancelar_compra_boton)
        self.debe_ver(self._cancelar_dialogo)
        self.click_boton(self._cancelar_compra_boton)
        self.debe_ver(self._compra_cancelada)
