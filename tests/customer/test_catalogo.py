from datos.prueba import TARJETA_VALIDA
from flows.compra import llegar_a_finalizar_compra
from pages.aplicacion import Aplicacion


class TestCatalogoPage:
    """Suite de pruebas para la pagina catálogo"""

    def test_compra_sin_pago(self, app: Aplicacion):
        llegar_a_finalizar_compra(app, aniadir_unidad=True, texto_ficha="Disponible")
        # click 'Confirmar pedido' y verificar pagina recibo abierta
        app.finalizar_compra.aceptar_condiciones()
        app.finalizar_compra.confirmar_pedido()
        app.recibo_pedido.debe_ver(app.recibo_pedido._texto_recibo)
        app.page.wait_for_timeout(3000)

    def test_compra_con_pago(self, app: Aplicacion):
        llegar_a_finalizar_compra(app, aniadir_unidad=False, texto_ficha="Chocorramo Unidad")
        app.finalizar_compra.elegir_pago_con_tarjeta()
        app.finalizar_compra.aceptar_condiciones()
        app.finalizar_compra.confirmar_pedido()
        # rellenando detalles tarjeta
        app.pago_tarjeta.debe_mostrar_formulario()
        app.pago_tarjeta.pagar_con_tarjeta(TARJETA_VALIDA)
        app.pago_tarjeta.debe_ver(app.pago_tarjeta._pago_confirmado)
        app.recibo_pedido.debe_ver(app.recibo_pedido._texto_producto_pagado, primero=True)
        app.page.wait_for_timeout(2000)

    def test_cancelar_compra(self, app: Aplicacion):
        llegar_a_finalizar_compra(app, aniadir_unidad=True, texto_ficha="Disponible")
        # click 'Cancelar compra' y verificar toast de compra cancelada
        app.finalizar_compra.cancelar_compra()
        app.page.wait_for_timeout(3000)
