from flows.cuenta import abrir_primer_pedido
from pages.aplicacion import Aplicacion


class TestMisPedidosPage:
    """Suite de pruebas para la pagina Mis Pedidos. Todas parten del detalle del primer pedido de la lista."""

    def test_mis_pedidos_pago_prueba(self, app: Aplicacion):
        # necesita que exista un pago pendiente, y que sea el primero de la lista
        abrir_primer_pedido(app)
        app.mi_cuenta.pedidos.pagar_con_pago_de_prueba()
        app.page.wait_for_timeout(3000)

    def test_mis_pedidos_pago_klarna(self, app: Aplicacion):
        # necesita que exista un pago pendiente, y que sea el primero de la lista
        abrir_primer_pedido(app)
        app.mi_cuenta.pedidos.pagar_con_tarjeta()

        # rellenando detalles Klarna
        pago = app.pago_tarjeta
        pago.debe_mostrar_formulario()
        pago.elegir_pestana("klarna")
        pago.boton_pagar(4).click()     # not that reliable
        pago.page.wait_for_timeout(2000)
        pago.debe_ver("We're here to make payments simple and flexible. Let's verify your number.")
        pago.fill_box("input[id='phone']", '+34695258314')
        pago.encontrar("button[id='onContinue']").click()
        pago.debe_ver("Enter the 6-digit code")
        pago.fill_box("input[id='otp_field']", "000000")
        pago.page.wait_for_timeout(2000)

    def test_mis_pedidos_pago_paypal(self, app: Aplicacion):
        # necesita que exista un pago pendiente, y que sea el primero de la lista
        abrir_primer_pedido(app)
        app.mi_cuenta.pedidos.pagar_con_tarjeta()

        # rellenando detalles PayPal
        pago = app.pago_tarjeta
        pago.debe_mostrar_formulario()
        pago.elegir_pestana("paypal")
        pago.page.wait_for_timeout(2000)
        pago.debe_ver("Se ha seleccionado PayPal.")
        pago.boton_pagar(4).click()     # not that reliable
        pago.debe_ver("Paypal test payment page")
        # pago.encontrar("button[id='authorize-test-payment-button']").click()  #data-testid!!!
        pago.page.wait_for_timeout(2000)

    def test_mis_pedidos_descargar_recibo_chat(self, app: Aplicacion):
        # No hace falta que exista un pedido con pago pendiente, este test funciona en cualquier pedido
        abrir_primer_pedido(app)
        # bajar recibo
        ruta_recibo = app.mi_cuenta.pedidos.descargar_recibo()
        assert ruta_recibo.exists(), f"El recibo no existe en la ruta: {ruta_recibo}"
        print(f"Recibo descargado en: {ruta_recibo}")
        app.mi_cuenta.abrir_archivo(ruta_recibo)

        # preguntar en chat
        chat = app.mi_cuenta.chat
        chat.abrir()
        chat.enviar("Como se realiza una devolucion?")
        chat.debe_mostrar("Como se realiza una devolucion?")
        app.page.wait_for_timeout(3000)

    def test_mis_pedidos_cancelar(self, app: Aplicacion):
        # necesita que el primer pedido de la lista no este cancelado. Se podria mejorar buscando el nombre del pedido
        abrir_primer_pedido(app)
        app.mi_cuenta.pedidos.cancelar_pedido()
        app.page.wait_for_timeout(3000)
