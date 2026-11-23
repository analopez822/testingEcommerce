from playwright.sync_api import Page

from components.lista_tarjetas import ListaTarjetas
from core.base_page import BasePage
from core.vocabulario import Boton, Campo, Panel


class PedidosSeccion(BasePage):
    """Mi cuenta > Mis pedidos: lista, detalle de un pedido, pagos, cancelacion, recibo y devolucion."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.lista = ListaTarjetas(page)

        # locators lista de pedidos
        self._pedidos_header: str = "Aquí tienes todo lo que has comprado."
        self._prefijo_pedido: str = "Pedido P-2026"
        self._boton_ver_detalle: str = "Ver detalle"
        self._link_volver_a_pedidos: str = "Volver a mis pedidos"

        # locators detalle: cancelar pedido
        self._boton_cancelar_pedido: str = "Cancelar pedido"
        self._dialogo_cancelar_pedido: str = "¿Cancelar el pedido "
        self._confirmacion_pedido_cancelado: str = " cancelado"

        # locators detalle: recibo
        self._boton_descargar_recibo: str = "Descargar recibo"

        # locators detalle: pago
        self._boton_pago_prueba: str = "Pago de prueba"
        self._dialogo_pago_prueba: str = "Esta pantalla imita a la pasarela real: elige el resultado y vuelve a la tienda."
        self._boton_pago_correcto: str = "Simular pago correcto"
        self._pago_completado: str = "Pago completado"

        # locators detalle: devolver pedido
        self._boton_devolver_pedido: str = "Devolver"
        self._dialogo_devolver_pedido: str = "Cuéntanos qué ha pasado. Revisaremos la solicitud y te diremos cómo enviarlo."
        self._motivo_devolucion: str = Campo.MOTIVO
        self._boton_enviar_solicitud: str = "Enviar solicitud"
        self._confirmacion_solicitud_devolucion: str = "Solicitud enviada"
        self._no_mas_devoluciones: str = "Este pedido ya no admite devoluciones."

    def abrir(self) -> None:
        self.click_link(Panel.MIS_PEDIDOS)
        self.debe_ver(self._pedidos_header)

    def describir(self) -> None:
        self.lista.describir("pedidos", "Informacion del pedido")

    def abrir_primer_pedido(self) -> str:
        """Entra en el detalle del primer pedido de la lista y devuelve su texto (ej: 'Pedido P-2026-4274')."""
        pedido = self.buscar_por_texto(self._prefijo_pedido).first.text_content()
        print(pedido)
        self.buscar_por_rol("link", name=self._boton_ver_detalle).first.click()
        self.debe_ver(self._link_volver_a_pedidos)
        return pedido

    def pagar_con_pago_de_prueba(self) -> None:
        self.click_boton(self._boton_pago_prueba)
        self.debe_ver(self._dialogo_pago_prueba)
        self.click_boton(self._boton_pago_correcto)
        self.debe_ver(self._pago_completado)

    def pagar_con_tarjeta(self) -> None:
        """Abre el formulario de pago seguro (tarjeta, Apple Pay, Google Pay, Klarna, PayPal)."""
        self.click_boton(Boton.PAGAR_CON_TARJETA)

    def cancelar_pedido(self) -> None:
        self.click_boton(self._boton_cancelar_pedido)
        self.debe_ver(self._dialogo_cancelar_pedido)
        self.click_boton(self._boton_cancelar_pedido)       # el boton del dialogo tiene el mismo nombre
        # TODO: comprobar f"{pedido} {self._confirmacion_pedido_cancelado}" (el test original no llegaba a afirmarlo)

    def descargar_recibo(self):
        """Descarga el recibo PDF y devuelve su ruta."""
        self.click_boton(self._boton_descargar_recibo)      # el test original pulsaba el boton antes de esperar la descarga
        return self.descargar_pdf(self._boton_descargar_recibo)

    def solicitar_devolucion(self, motivo: str) -> None:
        self.click_boton(self._boton_devolver_pedido)
        self.debe_ver(self._dialogo_devolver_pedido)
        self.fill_box(self._motivo_devolucion, motivo)
        self.click_boton(self._boton_enviar_solicitud)
        self.debe_ver(self._confirmacion_solicitud_devolucion)
        self.debe_ver(self._no_mas_devoluciones)
