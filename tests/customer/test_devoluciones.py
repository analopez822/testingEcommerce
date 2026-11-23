from playwright.sync_api import expect

from flows.auth import abrir_administracion, abrir_mi_cuenta
from flows.cuenta import abrir_primer_pedido
from pages.aplicacion import Aplicacion

# Fila de la tabla del superadmin que corresponde al pedido a devolver (numero de pedido + cliente).
# Hay que actualizarla a mano para que coincida con el primer pedido de la lista del cliente.
FILA_DEVOLUCION = "P-2026-4274 Ana Redondo"


class TestDevolucionesPage:
    """Suite de pruebas para la pagina Devoluciones"""

    def devoluciones(self, app: Aplicacion):
        """Ayuda (no es un test): lista por consola las devoluciones del cliente."""
        abrir_mi_cuenta(app)
        app.mi_cuenta.devoluciones.abrir()
        app.mi_cuenta.devoluciones.debe_ver_vista_cliente()
        app.mi_cuenta.devoluciones.describir()
        app.page.wait_for_timeout(2000)

    def test_solicitar_devolucion(self, app: Aplicacion):
        # este test necesita que haya al menos un pedido en la lista de pedidos
        # tambien necesita que FILA_DEVOLUCION (arriba) coincida con el pedido a devolver
        # se requiere que haya una sesion abierta para el usuario, y ver la lista de pedidos
        # y una segunda sesion para el super admin, para ver Devoluciones y aprobarlas
        abrir_primer_pedido(app)
        app.mi_cuenta.pedidos.solicitar_devolucion("El producto no cumple con las expectativas")

        # abrir otro browser en incognito para logearse como super admin y aprobar la devolucion
        app.login.debugger()
        admin = app.nueva_sesion()
        abrir_administracion(admin)
        # abriendo Devoluciones, aprobando, marcando como recibida y reembolsando
        devoluciones = admin.mi_cuenta.devoluciones
        devoluciones.abrir()
        devoluciones.debe_ver_vista_superadmin()
        devoluciones.aprobar(FILA_DEVOLUCION, "Devolucion aprobada")
        devoluciones.marcar_recibida(FILA_DEVOLUCION)
        devoluciones.reembolsar(FILA_DEVOLUCION)

        # comprobando en primer browser que el pedido ha sido reembolsado
        app.page.bring_to_front()
        app.mi_cuenta.pedidos.abrir()
        expect(app.mi_cuenta.pedidos.lista.items.first).to_contain_text("Reembolsado")
