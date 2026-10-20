from playwright.sync_api import expect

from conftest import app_catalogo, app_login, app_navegacion, app_finalizar_compra
from pages.shared.pago_tarjeta_page import PagoTarjetaPage
from pages.shared.recibo_pedido_page import ReciboPedidoPage
from pages.shared.catalogo_page import CatalogoPage
from pages.shared.finalizar_compra_page import FinalizarCompraPage
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage

class TestCatalogoPage:
    """Suite de pruebas para la pagina catálogo"""

    def test_compra_sin_pago(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_catalogo: CatalogoPage, app_finalizar_compra: FinalizarCompraPage, app_recibo_pedido: ReciboPedidoPage):
        # abro en browser, hago click en Catalogo y una search de chocorramo
        app_login.navegar()
        app_navegacion.click_link(app_navegacion._catalogo_boton)
        expect(app_catalogo.buscar_por_texto(app_catalogo._texto_catalogo)).to_be_visible()
        app_catalogo.fill_box(app_catalogo._cajita_busqueda, "chocorramo")
        # click en producto chocorramo, añado una unidad mas, click 'Añadir al carrito'. Verificar toast de 'añadido'
        app_catalogo.encontrar("a[href='/catalogo/producto-chocorramo']").nth(0).click()
        expect(app_catalogo.buscar_por_texto("Disponible")).to_be_visible()
        app_catalogo.click_boton(app_catalogo._boton_aniadir_unidad)
        app_catalogo.click_boton(app_catalogo._boton_aniadir_carrito)
        expect(app_catalogo.buscar_por_texto("\"Chocorramo Unidad\" añadido al carrito")).to_be_visible()
        # click icono carrito y 'Finalizar compra', verificar que formulario de login aparece
        app_navegacion.buscar_por_rol("link", name=app_navegacion._carrito_boton).click()
        expect(app_catalogo.buscar_por_texto("Tu carrito se guarda en este navegador. Inicia sesión para llevarlo contigo.")).to_be_visible()
        app_catalogo.click_link(app_catalogo._boton_finalizar_compra)
        # app_catalogo.encontrar("a[href='/checkout']").click()  ==> igual que linea 28
        # app_catalogo.buscar_por_rol("link", name=app_catalogo._boton_finalizar_compra).click()  ==> igual que linea 28
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        # rellenando formulario login y verificando pantalla 'Finalizar compra' aparece
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._texto_finalizar_compra)).to_be_visible()
        # rellenando 'Finalizar compra', guardando direccion y verificando toast 'direccion guardada'
        app_finalizar_compra.fill_box(app_finalizar_compra._nombre, "Ana Maria")
        app_finalizar_compra.page.locator("button[role='combobox']").nth(1).click()
        app_finalizar_compra.fill_box(app_finalizar_compra._ciudad, "Madrid")
        app_finalizar_compra.page.locator("ul[class='max-h-64 overflow-y-auto p-1']").locator("button").first.click()
        app_finalizar_compra.fill_box(app_finalizar_compra._direccion, "Calle Falsa 123")
        app_finalizar_compra.fill_box(app_finalizar_compra._codigo_postal, "12345")
        app_finalizar_compra.fill_box(app_finalizar_compra._provincia, "Madrid")
        app_finalizar_compra.fill_box(app_finalizar_compra._telefono, "123456789")
        app_finalizar_compra.fill_box(app_finalizar_compra._notas_entrega, "Notas de entrega")
        app_finalizar_compra.click_boton(app_finalizar_compra._guardar_direccion_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._direccion_guardada)).to_be_visible()
        # click 'Confirmar pedido' y verificar pagina recibo abierta
        app_finalizar_compra.encontrar(app_finalizar_compra._condiciones).check()
        app_finalizar_compra.encontrar(app_finalizar_compra._desistimiento).click()
        app_finalizar_compra.click_boton(app_finalizar_compra._confirmar_pedido_boton)
        expect(app_recibo_pedido.buscar_por_texto(app_recibo_pedido._texto_recibo)).to_be_visible()
        app_catalogo.page.wait_for_timeout(3000)

    def test_compra_con_pago(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_catalogo: CatalogoPage,
                             app_finalizar_compra: FinalizarCompraPage, app_recibo_pedido: ReciboPedidoPage, app_pago_tarjeta: PagoTarjetaPage):
        # abro en browser, hago click en Catalogo y una search de chocorramo
        app_login.navegar()
        app_navegacion.click_link(app_navegacion._catalogo_boton)
        expect(app_catalogo.buscar_por_texto(app_catalogo._texto_catalogo)).to_be_visible()
        app_catalogo.fill_box(app_catalogo._cajita_busqueda, "chocorramo")
        # click en producto chocorramo, añado una unidad mas, click 'Añadir al carrito'. Verificar toast de 'añadido'
        app_catalogo.encontrar("a[href='/catalogo/producto-chocorramo']").nth(0).click()
        expect(app_catalogo.buscar_por_texto("Disponible")).to_be_visible()
        app_catalogo.click_boton(app_catalogo._boton_aniadir_unidad)
        app_catalogo.click_boton(app_catalogo._boton_aniadir_carrito)
        expect(app_catalogo.buscar_por_texto("\"Chocorramo Unidad\" añadido al carrito")).to_be_visible()
        # click icono carrito y 'Finalizar compra', verificar que formulario de login aparece
        app_navegacion.buscar_por_rol("link", name=app_navegacion._carrito_boton).click()
        expect(app_catalogo.buscar_por_texto("Tu carrito se guarda en este navegador. Inicia sesión para llevarlo contigo.")).to_be_visible()
        app_catalogo.click_link(app_catalogo._boton_finalizar_compra)
        # app_catalogo.encontrar("a[href='/checkout']").click()  ==> igual que linea 28
        # app_catalogo.buscar_por_rol("link", name=app_catalogo._boton_finalizar_compra).click()  ==> igual que linea 28
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        # rellenando formulario login y verificando pantalla 'Finalizar compra' aparece
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._texto_finalizar_compra)).to_be_visible()
        # rellenando 'Finalizar compra', guardando direccion y verificando toast 'direccion guardada'
        app_finalizar_compra.fill_box(app_finalizar_compra._nombre, "Ana Maria")
        app_finalizar_compra.page.locator("button[role='combobox']").nth(1).click()
        app_finalizar_compra.fill_box(app_finalizar_compra._ciudad, "Madrid")
        app_finalizar_compra.page.locator("ul[class='max-h-64 overflow-y-auto p-1']").locator("button").first.click()
        app_finalizar_compra.fill_box(app_finalizar_compra._direccion, "Calle Falsa 123")
        app_finalizar_compra.fill_box(app_finalizar_compra._codigo_postal, "12345")
        app_finalizar_compra.fill_box(app_finalizar_compra._provincia, "Madrid")
        app_finalizar_compra.fill_box(app_finalizar_compra._telefono, "123456789")
        app_finalizar_compra.fill_box(app_finalizar_compra._notas_entrega, "Notas de entrega")
        app_finalizar_compra.click_boton(app_finalizar_compra._guardar_direccion_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._direccion_guardada)).to_be_visible()
        # click 'Confirmar pedido' y verificar pagina recibo abierta
        app_finalizar_compra.buscar_por_texto(app_finalizar_compra._tarjeta_boton).click()
        app_finalizar_compra.encontrar(app_finalizar_compra._condiciones).check()
        app_finalizar_compra.encontrar(app_finalizar_compra._desistimiento).click()
        app_finalizar_compra.click_boton(app_finalizar_compra._confirmar_pedido_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._pedido_creado))
        # rellenando detalles tarjeta
        expect(app_pago_tarjeta.buscar_por_texto(app_pago_tarjeta._formulario_pago_tarjeta).first).to_be_visible()
        card_iframe = app_pago_tarjeta.page.frame_locator("iframe[title='Campo de entrada seguro para el pago']")
        card_iframe.locator("input[id='payment-numberInput']").fill("4242424242424242")
        card_iframe.locator("input[id='payment-expiryInput']").fill("12/26")
        card_iframe.locator("input[id='payment-cvcInput']").fill("123")
        card_iframe.locator("select[id='payment-countryInput']").select_option("Albania")
        card_iframe.locator("input[id='payment-linkEmailInput']").fill("correo@yahoo.es")
        card_iframe.locator("input[id='payment-linkMobilePhoneInput']").fill("07400123456")
        card_iframe.locator("input[id='payment-linkLegalNameInput']").fill("Ana Redondo")
        # card_iframe.locator("button[class='group/button inline-flex shrink-0 items-center justify-center rounded-lg border border-transparent bg-clip-padding text-sm font-medium whitespace-nowrap transition-all outline-none select-none focus-visible:border-ring focus-visible:ring-3']").click() #app_pago_tarjeta._boton_pagar
        boton_pagar = app_pago_tarjeta.buscar_por_texto("Pagar ").nth(2)
        expect(boton_pagar).to_be_visible()
        boton_pagar.click()
        # app_pago_tarjeta.page.wait_for_timeout(3000)
        expect(app_pago_tarjeta.buscar_por_texto("Pago confirmado")).to_be_visible()
        expect(app_recibo_pedido.buscar_por_texto(app_recibo_pedido._texto_producto_pagado).first).to_be_visible()
        app_recibo_pedido.page.wait_for_timeout(3000)

    def test_cancelar_compra(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_catalogo: CatalogoPage, app_finalizar_compra: FinalizarCompraPage, app_recibo_pedido: ReciboPedidoPage):
        # abro en browser, hago click en Catalogo y una search de chocorramo
        app_login.navegar()
        app_navegacion.click_link(app_navegacion._catalogo_boton)
        expect(app_catalogo.buscar_por_texto(app_catalogo._texto_catalogo)).to_be_visible()
        app_catalogo.fill_box(app_catalogo._cajita_busqueda, "chocorramo")
        # click en producto chocorramo, añado una unidad mas, click 'Añadir al carrito'. Verificar toast de 'añadido'
        app_catalogo.encontrar("a[href='/catalogo/producto-chocorramo']").nth(0).click()
        expect(app_catalogo.buscar_por_texto("Disponible")).to_be_visible()
        app_catalogo.click_boton(app_catalogo._boton_aniadir_unidad)
        app_catalogo.click_boton(app_catalogo._boton_aniadir_carrito)
        expect(app_catalogo.buscar_por_texto("\"Chocorramo Unidad\" añadido al carrito")).to_be_visible()
        # click icono carrito y 'Finalizar compra', verificar que formulario de login aparece
        app_navegacion.buscar_por_rol("link", name=app_navegacion._carrito_boton).click()
        expect(app_catalogo.buscar_por_texto("Tu carrito se guarda en este navegador. Inicia sesión para llevarlo contigo.")).to_be_visible()
        app_catalogo.click_link(app_catalogo._boton_finalizar_compra)
        # app_catalogo.encontrar("a[href='/checkout']").click()  ==> igual que linea 28
        # app_catalogo.buscar_por_rol("link", name=app_catalogo._boton_finalizar_compra).click()  ==> igual que linea 28
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        # rellenando formulario login y verificando pantalla 'Finalizar compra' aparece
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._texto_finalizar_compra)).to_be_visible()
        # rellenando 'Finalizar compra', guardando direccion y verificando toast 'direccion guardada'
        app_finalizar_compra.fill_box(app_finalizar_compra._nombre, "Ana Maria")
        app_finalizar_compra.page.locator("button[role='combobox']").nth(1).click()
        app_finalizar_compra.fill_box(app_finalizar_compra._ciudad, "Madrid")
        app_finalizar_compra.page.locator("ul[class='max-h-64 overflow-y-auto p-1']").locator("button").first.click()
        app_finalizar_compra.fill_box(app_finalizar_compra._direccion, "Calle Falsa 123")
        app_finalizar_compra.fill_box(app_finalizar_compra._codigo_postal, "12345")
        app_finalizar_compra.fill_box(app_finalizar_compra._provincia, "Madrid")
        app_finalizar_compra.fill_box(app_finalizar_compra._telefono, "123456789")
        app_finalizar_compra.fill_box(app_finalizar_compra._notas_entrega, "Notas de entrega")
        app_finalizar_compra.click_boton(app_finalizar_compra._guardar_direccion_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._direccion_guardada)).to_be_visible()
        # click 'Cancelar comprar' y verificar toast de compra cancelada
        app_finalizar_compra.click_boton(app_finalizar_compra._cancelar_compra_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._cancelar_dialogo)).to_be_visible()
        app_finalizar_compra.click_boton(app_finalizar_compra._cancelar_compra_boton)
        expect(app_finalizar_compra.buscar_por_texto(app_finalizar_compra._compra_cancelada)).to_be_visible()
        app_catalogo.page.wait_for_timeout(3000)


