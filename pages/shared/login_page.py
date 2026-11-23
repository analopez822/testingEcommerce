from core.base_page import BasePage
from core.config import Usuario
from core.vocabulario import Boton, Campo, Mensaje
from playwright.sync_api import Page

class LoginPage(BasePage):
    """
        Clase con los locators y metodos de login
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators formulario login
        self._entrar_llave_acceso: str = "Entrar con llave de acceso"
        self._texto: str = "Accede a tu cuenta para comprar y seguir tus pedidos."
        self._email: str = Campo.EMAIL
        self._password: str = Campo.PASSWORD
        self._mantener_sesion: str = "Mantener la sesión en este dispositivo"
        self._boton_ocultar_contrasenia: str = "Ocultar contraseña"
        self._boton_contrasenia: str = "Mostrar contraseña"
        self._boton_entrar: str = "Entrar"
        self._link_olvidaste_contrasenia: str = "¿Has olvidado tu contraseña?"
        self._link_crear_cuenta: str = Boton.CREAR_CUENTA
        self._login_fallido: str = "Email o contraseña incorrectos"

        # locators pagina super admin
        self._login_exito: str = "Hola de nuevo, "
        self._icono_usuario: str = "SA"

        # locators popup de reset password
        self._reset_password: str = "Introduce tu email y te enviaremos un código."
        self._boton_enviar_codigo: str = "Enviar código"
        self._link_volver_a_iniciar_sesion: str = Boton.VOLVER_A_INICIAR_SESION
        self._popup_introducir_codigo: str = "Introduce el código enviado a "

        # locators popup de introducir codigo
        self._caja_codigo: str = Campo.CODIGO_OTP
        self._boton_continuar: str = "Continuar"
        self._popup_demasiados_intentos: str = Mensaje.DEMASIADOS_INTENTOS
        self._codigo_incorrecto: str = "El código es incorrecto o ha caducado"

        # locators formulario crear cuenta
        self._crear_cuenta: str = "Te enviaremos un código para verificar tu email."
        self._nombre: str = "input[name='firstName']"
        self._apellidos: str = "input[name='lastName']"
        self._repite_contrasenia: str = "input[name='confirmPassword']"
        self._tickbox_terminos: str = "Acepto los términos y condiciones y la política de privacidad"
        self._boton_crear_cuenta: str = Boton.CREAR_CUENTA

        # locator formulario nueva contrasenia
        self._contrasenia_nueva: str = "Elige una nueva contraseña."
        self._password_string: str = "nueva-contraseña123"
        self._boton_guardar_contrasenia: str = "Guardar contraseña"
        self._mensaje_contrasenia_actualizada: str = "Contraseña actualizada"

        self._verifica_correo_nuevo: str = "Introduce el código de 6 dígitos"
        self._boton_verificar: str = "Verificar"
        self._confirmacion_correo_nuevo: str = "Email verificado. Ya puedes iniciar sesión."

    def debe_mostrar_formulario(self) -> None:
        self.debe_ver(self._texto)

    def alternar_mantener_sesion(self) -> None:
        self.buscar_por_rol("checkbox", name=self._mantener_sesion).click()

    def enviar_credenciales(self, email: str, contrasenia: str) -> None:
        """Rellena el formulario y pulsa Entrar (sin comprobar el resultado: sirve para login correcto y fallido)."""
        self.fill_box(self._email, email)
        self.fill_box(self._password, contrasenia)
        # hay dos botones 'Entrar' en la pagina (barra y formulario): el del formulario es el segundo
        self.buscar_por_rol("button", name=self._boton_entrar).nth(1).click()

    def iniciar_sesion(self, usuario: Usuario) -> None:
        """Login correcto: envia credenciales y comprueba el toast de bienvenida."""
        self.enviar_credenciales(usuario.email, usuario.contrasenia)
        self.debe_ver(self._login_exito)

    def click_boton_contrasenia(self, status: str) -> None:
        if status == "Mostrar contraseña":
            self.page.get_by_role("button", name=self._boton_contrasenia).click()
        elif status == "Ocultar contraseña":
            self.page.get_by_role("button", name=self._boton_ocultar_contrasenia).click()
