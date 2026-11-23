from playwright.sync_api import Page

from components.ag_grid import AgGrid
from components.lista_tarjetas import ListaTarjetas
from core.base_page import BasePage
from core.vocabulario import Panel


class DevolucionesSeccion(BasePage):
    """
    Devoluciones. El cliente ve su lista; el superadmin ve una tabla AG Grid con las solicitudes
    y las resuelve con el menu 'Acciones' de cada fila (aprobar, marcar recibida, reembolsar).
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.lista = ListaTarjetas(page)
        self.grid = AgGrid(page)

        # vista cliente / vista superadmin
        self._header_cliente: str = "Lo que has pedido devolver y en qué punto está."
        self._header_superadmin: str = "Solicitudes de los clientes y su resolución."

        # aprobar
        self._dialogo_aprobar_devolucion: str = "Mensaje para el cliente"   # titulo del dialogo y nombre de su caja de texto
        self._boton_aprobar: str = "Aprobar"
        self._devolucion_aprobada: str = "Devolución aprobada"

        # recibida
        self._boton_marcar_recibida: str = "Marcar como recibida"
        self._stock_repuesto: str = "Recibida: stock repuesto"

        # reembolsar (dos dialogos seguidos, ambos con boton 'Reembolsar')
        self._boton_reembolsar: str = "Reembolsar"
        self._dialogo_reembolso_paso1: str = "Por defecto se devuelve el precio de las unidades menos la comisión de la política."
        self._dialogo_reembolso_paso2: str = "Reembolsar la devolución"
        self._reembolso_enviado: str = "Reembolso enviado"

    def abrir(self) -> None:
        self.click_link(Panel.DEVOLUCIONES)

    def debe_ver_vista_cliente(self) -> None:
        self.debe_ver(self._header_cliente)

    def debe_ver_vista_superadmin(self) -> None:
        self.debe_ver(self._header_superadmin)

    def describir(self) -> None:
        self.lista.describir("devoluciones", "Devolucion")

    def aprobar(self, fila: str, mensaje: str) -> None:
        self.grid.accion_en_fila(fila, self._boton_aprobar)
        self.debe_ver(self._dialogo_aprobar_devolucion)
        self.buscar_por_rol("textbox", name=self._dialogo_aprobar_devolucion).fill(mensaje)
        self.buscar_por_rol("button", name=self._boton_aprobar).click()
        self.debe_ver(self._devolucion_aprobada)

    def marcar_recibida(self, fila: str) -> None:
        self.grid.accion_en_fila(fila, self._boton_marcar_recibida)
        self.debe_ver(self._stock_repuesto)

    def reembolsar(self, fila: str) -> None:
        self.grid.accion_en_fila(fila, self._boton_reembolsar)
        self.debe_ver(self._dialogo_reembolso_paso1)
        self.buscar_por_rol("button", name=self._boton_reembolsar).click()
        self.debe_ver(self._dialogo_reembolso_paso2)
        self.buscar_por_rol("button", name=self._boton_reembolsar).click()
        self.debe_ver(self._reembolso_enviado)
