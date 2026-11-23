from core import config
from pages.aplicacion import Aplicacion


class TestLoginPage:
    """Suite de pruebas para la pagina login"""

    def test_login_exito(self, app: Aplicacion):
        nav, login = app.navegacion, app.login
        login.debugger()
        login.navegar()
        nav.ir_a_login()
        login.debe_mostrar_formulario()
        login.alternar_mantener_sesion()
        login.alternar_mantener_sesion()
        login.iniciar_sesion(config.usuario("customer"))
        nav.comprobar_menu_usuario(
            visibles=[nav._mi_cuenta, nav._cerrar_sesion],
            ocultas=[nav._administracion, nav._configuracion],
        )
        login.page.wait_for_timeout(3000)

    def test_login_fallido(self, app: Aplicacion):
        login = app.login
        login.navegar()
        app.navegacion.ir_a_login()
        login.debe_mostrar_formulario()
        login.enviar_credenciales(config.usuario("customer").email, config.CONTRASENIA_INCORRECTA)
        login.debe_ver(login._login_fallido)

    def test_entrar_con_llave_acceso(self, app: Aplicacion):
        """ Requiere meter manualmente la contraseña del ordenador
        Este es el unico usuario configurado para entrar con llave de acceso """
        login = app.login
        login.navegar()
        app.navegacion.ir_a_login()
        login.debe_mostrar_formulario()
        login.buscar_por_rol("button", name=login._entrar_llave_acceso).click()
        login.page.wait_for_timeout(3000)
        login.debe_ver("Hola de nuevo, Ana")

    # def test_reset_password(self, app: Aplicacion):
    #     """ Requiere meter manualmente el codigo enviado al correo
    #     Tambien requiere resetear manualmente la contrasenia cada vez que el test se ejecuta, para
    #     que sea la misma que hay en el .env """
    #     login = app.login
    #     usuario = config.usuario("customer")
    #     login.navegar()
    #     app.navegacion.ir_a_login()
    #     login.debe_mostrar_formulario()
    #     login.buscar_por_rol("link", name=login._link_olvidaste_contrasenia).click()
    #     login.debe_ver(login._reset_password)
    #     login.fill_box(login._email, usuario.email)
    #     login.buscar_por_rol("button", name=login._boton_enviar_codigo).click()
    #     login.debe_ver(login._popup_introducir_codigo)
    #     codigo = input("Introduce el código de verificación recibido por correo electrónico: ")
    #     login.fill_box(login._caja_codigo, codigo)
    #     login.buscar_por_rol("button", name=login._boton_continuar).click()
    #     login.page.wait_for_timeout(3000)
    #     login.debe_ver(login._contrasenia_nueva)
    #     login.fill_box(login._password, login._password_string)
    #     login.fill_box(login._repite_contrasenia, login._password_string)
    #     login.buscar_por_rol("button", name=login._boton_guardar_contrasenia).click()
    #     login.debe_ver(login._mensaje_contrasenia_actualizada)
    #     login.iniciar_sesion(Usuario("customer", usuario.email, login._password_string))   # from core.config import Usuario
    #     login.page.wait_for_timeout(4000)

    # def test_reset_password_demasiados_intentos(self, app: Aplicacion):
    #     """ Crear codigo para 3 intentos fallidos de reset password, para que salga el popup demasiados intentos"""
    #     login = app.login                    # requiere intentar cambiar la password varias veces manualmente para reprodocir escenario
    #     login.navegar()
    #     app.navegacion.ir_a_login()
    #     login.debe_mostrar_formulario()
    #     login.buscar_por_rol("link", name=login._link_olvidaste_contrasenia).click()
    #     login.debe_ver(login._reset_password)
    #     login.fill_box(login._email, config.usuario("customer").email)
    #     login.buscar_por_rol("button", name=login._boton_enviar_codigo).click()
    #     login.debe_ver(login._popup_demasiados_intentos)
    #     login.page.wait_for_timeout(4000)

    def test_reset_password_volver_a_iniciar_sesion(self, app: Aplicacion):
        login = app.login
        login.navegar()
        app.navegacion.ir_a_login()
        login.debe_mostrar_formulario()
        login.buscar_por_rol("link", name=login._link_olvidaste_contrasenia).click()
        login.debe_ver(login._reset_password)
        login.fill_box(login._email, config.usuario("superadmin").email)
        login.buscar_por_rol("link", name=login._link_volver_a_iniciar_sesion).click()
        login.debe_mostrar_formulario()
        login.page.wait_for_timeout(2000)
