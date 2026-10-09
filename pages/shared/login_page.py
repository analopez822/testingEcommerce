from core.base_page import BasePage
from playwright.sync_api import Page

class LoginPage(BasePage):
    """
        Clase con los locators y metodos de login
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina login
        self._entrar_llave_acceso: str = "Entrar con llave de acceso"
        self._texto: str = "Accede a tu cuenta para comprar y seguir tus pedidos."
        self._email: str = "input[name='email']"
        self._password: str = "input[name='password']"   #"input[id='_r_q_-input']"
        self._boton_ocultar_contrasenia: str = "Ocultar contraseña"
        self._boton_contrasenia: str = "Mostrar contraseña"
        self._boton_entrar: str = "Entrar"
        self._link_olvidaste_contrasenia: str = "¿Has olvidado tu contraseña?"
        self._link_crear_cuenta: str = "Crear cuenta"
        self._login_fallido: str = "Email o contraseña incorrectos"

        # locators pagina super admin
        self._login_exito: str = "Hola de nuevo, Super"

        # locators popup de reset password
        self._reset_password: str = "Introduce tu email y te enviaremos un código."
        self._boton_enviar_codigo: str = "Enviar código"
        self._link_volver_a_iniciar_sesion: str = "Volver a iniciar sesión"
        self._popup_introducir_codigo: str = "Introduce el código enviado a "

        # locators popup de introducir codigo
        self._caja_codigo: str = "input[autocomplete='one-time-code']"
        self._boton_continuar: str = "Continuar"
        self._link_iniciar_sesion: str = "Volver a iniciar sesión"
        self._popup_demasiados_intentos: str = "Demasiados intentos. Inténtalo más tarde."
        self._codigo_incorrecto: str = "El código es incorrecto o ha caducado"

        # locators formulario crear cuenta
        self._crear_cuenta: str = "Te enviaremos un código para verificar tu email."
        self._nombre: str = "input[name='firstName']"
        self._apellidos: str = "input[name='lastName']"
        self._email: str = "input[name='email']"
        self._contrasenia: str = "input[name='password']"
        self._repite_contrasenia: str = "input[name='confirmPassword']"
        self._tickbox_terminos: str = "Acepto los términos y condiciones y la política de privacidad"
        self._boton_crear_cuenta: str = "Crear cuenta"

        # locator formulario nueva contrasenia
        self._contrasenia_nueva: str = "Elige una nueva contraseña."
        self._password_string: str = "contraseña123"
        self._boton_guardar_contrasenia: str = "Guardar contraseña"
        self._mensaje_contrasenia_actualizada: str = "Contraseña actualizada correctamente"
        self._demasiados_intentos: str = "Demasiados intentos. Inténtalo más tarde."

        self._verifica_correo_nuevo: str = "Introduce el código de 6 dígitos"
        self._boton_verificar: str = "Verificar"
        self._confirmacion_correo_nuevo: str = "Email verificado. Ya puedes iniciar sesión."



    def click_boton_contrasenia(self, status: str) -> None:
        if status == "Mostrar contraseña":
            self.page.get_by_role("button", name=self._boton_contrasenia).click()
        elif status == "Ocultar contraseña":
            self.page.get_by_role("button", name=self._boton_ocultar_contrasenia).click()




