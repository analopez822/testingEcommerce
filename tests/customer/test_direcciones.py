from datos.prueba import DIRECCION_EDITADA
from flows.cuenta import abrir_direcciones
from pages.aplicacion import Aplicacion


class TestDireccionesPage:
    """Suite de pruebas para la pagina Direcciones"""

    def test_direcciones_eliminar(self, app: Aplicacion):
        # este test necesita que haya al menos dos direcciones en la lista
        abrir_direcciones(app)
        # borra la segunda direccion de la lista
        app.mi_cuenta.direcciones.eliminar(1)

    def test_direcciones_editar(self, app: Aplicacion):
        # este test necesita que haya al menos una direccion en la lista
        abrir_direcciones(app)
        # edita la primera direccion de la lista (el dialogo de editar reutiliza el formulario de Finalizar compra)
        app.mi_cuenta.direcciones.abrir_edicion(0)
        app.finalizar_compra.editar_contacto(DIRECCION_EDITADA)
        app.page.wait_for_timeout(2000)
