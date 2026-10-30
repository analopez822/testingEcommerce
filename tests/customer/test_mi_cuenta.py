from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestMiCuentaPage:
    """Suite de pruebas para la pagina login"""

    def test_mi_cuenta(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # app_login.debugger()
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_login._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        app_navegacion.click_boton(app_navegacion._menu_usuario_boton)
        app_navegacion.buscar_por_rol("menuitem", name=app_navegacion._mi_cuenta).click()
        # app_navegacion.buscar_por_rol("menuitem", name=app_navegacion._cerrar_sesion).click()
        # comprobando titulo y secciones de Mis Datos
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._mis_datos, exact=True)).to_be_visible()
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._datos_personales)).to_be_visible()
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._correo)).to_be_visible()
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._descargar_datos)).to_be_visible()
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._eliminar_cuenta)).to_be_visible()
        # comprobando elementos de panel izquierdo: abriendo y verificando titulo
        app_mi_cuenta.click_link(app_mi_cuenta._mis_datos)
        app_mi_cuenta.click_link(app_mi_cuenta._mis_pedidos)
        app_mi_cuenta.click_link(app_mi_cuenta._direcciones)
        app_mi_cuenta.click_link(app_mi_cuenta._metodos_pago)
        app_mi_cuenta.click_link(app_mi_cuenta._devoluciones)
        app_mi_cuenta.click_link(app_mi_cuenta._suscripcion)
        app_mi_cuenta.click_link(app_mi_cuenta._juega_gana)
        app_mi_cuenta.click_link(app_mi_cuenta._seguridad)
        app_mi_cuenta.click_link(app_mi_cuenta._soporte)
        app_login.page.wait_for_timeout(2000)


    def test_mis_datos(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        app_login.debugger()
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, app_mi_cuenta._correo_usuario)
        app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()
        app_navegacion.click_boton(app_navegacion._menu_usuario_boton)
        app_navegacion.buscar_por_rol("menuitem", name=app_navegacion._mi_cuenta).click()
        # comprobando titulo y secciones de Mis Datos
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._mis_datos, exact=True)).to_be_visible()
        # actualizando telefono en Datos Personales
        app_mi_cuenta.fill_box(app_mi_cuenta._telefono, "123456789")
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_guardar_cambios)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._datos_actualizados)).to_be_visible()

        # # actualizando correo en Correo Electronico
        # Comento esta seccion porque requiere un cambio manual de correo electronico cada vez que se ejecuta
        # app_mi_cuenta.fill_box(app_mi_cuenta._nuevo_email, app_mi_cuenta._correo_admin)
        # app_mi_cuenta.fill_box(app_mi_cuenta._nueva_contrasenia, app_mi_cuenta._contrasenia_usuario)
        # app_mi_cuenta.click_boton(app_mi_cuenta._boton_correo)
        # expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._email_con_codigo_enviado)).to_be_visible()
        # codigo = input("Tienes un cambio pendiente a yihohic791@playfine.com. Escribe el código que te hemos enviado.")
        # app_mi_cuenta.fill_box(app_mi_cuenta._codigo_verificacion_correo, codigo)
        # app_mi_cuenta.click_boton(app_mi_cuenta._boton_confirmar)
        # app_login.page.wait_for_timeout(2000)
        # expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._email_actualizado)).to_be_visible()
        # app_login.page.wait_for_timeout(2000)

        # Descargando json file desde Descargar mis Datos
        ruta_datos = app_mi_cuenta.descargar_archivo_json(app_mi_cuenta._boton_descargar_json)
        assert ruta_datos.exists(), f"El archivo json no existe en el directorio: {ruta_datos}"
        print(f"Datos descargados en: {ruta_datos}")
        app_mi_cuenta.abrir_archivo(ruta_datos)

        # Eliminando cuenta desde Eliminar Cuenta
        app_mi_cuenta.fill_box(app_mi_cuenta._porque_te_vas, "Me doy de baja")
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_solicitar_baja)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._cancelar_cuenta)).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_cancelar)
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_solicitar_baja)
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_solicitar_baja)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._codigo_cancelacion_cuenta)).to_be_visible()
        codigo_baja = input("Escribe el código de verificacion de cambio de cuenta que te hemos enviado.")
        app_mi_cuenta.fill_box(app_mi_cuenta._codigo_verificacion_correo, codigo_baja)
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_confirmar_baja)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._baja_confirmada_mensaje).first).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_cancelar_baja)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._baja_cancelada)).to_be_visible()
        app_mi_cuenta.page.wait_for_timeout(2000)


