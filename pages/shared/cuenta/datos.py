from pathlib import Path

from playwright.sync_api import Page, expect

from core.base_page import BasePage
from core.vocabulario import Boton, Campo, Panel


class DatosSeccion(BasePage):
    """Mi cuenta > Mis datos: datos personales, cambio de email, descarga de datos y baja de la cuenta."""

    def __init__(self, page: Page):
        super().__init__(page)

        # locators Mis datos
        self._titulo: str = Panel.MIS_DATOS
        self._texto_mis_datos: str = "Tu información personal y cómo entras en la tienda."
        self._datos_personales: str = "Datos personales"
        self._telefono: str = Campo.TELEFONO
        self._boton_guardar_cambios: str = "Guardar cambios"
        self._datos_actualizados: str = "Datos actualizados"

        # locators cambio de correo
        self._correo: str = "Correo electrónico"
        self._nuevo_email: str = "input[name='newEmail']"
        self._nueva_contrasenia: str = Campo.PASSWORD
        self._boton_correo: str = "Cambiar email"
        self._email_con_codigo_enviado: str = "Te hemos enviado un código a "
        self._email_actualizado: str = "Email actualizado"
        self._codigo_verificacion_correo: str = "input[autocomplete='one-time-code'][data-slot='input-otp']"
        self._boton_confirmar: str = "Confirmar"

        # locators descarga de datos
        self._descargar_datos: str = "Descargar mis datos"

        # locators eliminar cuenta (baja)
        self._eliminar_cuenta: str = "Eliminar mi cuenta"
        self._porque_te_vas: str = Campo.MOTIVO
        self._boton_solicitar_baja: str = "Solicitar la baja"
        self._cancelar_cuenta: str = "Solicitar la baja de tu cuenta"            # titulo del dialogo
        self._codigo_cancelacion_cuenta: str = "Te hemos enviado un código para "
        self._boton_confirmar_baja: str = "Confirmar la baja"
        self._baja_confirmada_mensaje: str = "Tu cuenta se eliminará "
        self._boton_cancelar_baja: str = "Cancelar la baja"
        self._baja_cancelada: str = "Hemos cancelado la baja de tu cuenta"

    def abrir(self) -> None:
        self.click_link(Panel.MIS_DATOS)

    def debe_mostrar_titulo(self) -> None:
        expect(self.buscar_por_rol("heading", name=self._titulo, exact=True)).to_be_visible()

    def debe_mostrar_secciones(self) -> None:
        """Titulo y los bloques de la pagina Mis datos."""
        self.debe_mostrar_titulo()
        for encabezado in (self._datos_personales, self._correo, self._descargar_datos, self._eliminar_cuenta):
            expect(self.buscar_por_rol("heading", name=encabezado)).to_be_visible()

    def actualizar_telefono(self, telefono: str) -> None:
        self.fill_box(self._telefono, telefono)
        self.click_boton(self._boton_guardar_cambios)
        self.debe_ver(self._datos_actualizados)

    def descargar_mis_datos(self) -> Path:
        """Pulsa 'Descargar JSON', lo guarda en Descargas y devuelve la ruta."""
        return self.descargar_archivo_json(Boton.DESCARGAR_JSON)

    # --- baja de la cuenta: se divide en pasos porque el test debe introducir un codigo recibido por correo ---
    def abrir_dialogo_baja(self, motivo: str) -> None:
        self.fill_box(self._porque_te_vas, motivo)
        self.click_boton(self._boton_solicitar_baja)
        self.debe_ver(self._cancelar_cuenta)

    def cerrar_dialogo_baja(self) -> None:
        self.click_boton(Boton.CANCELAR)

    def pedir_codigo_baja(self) -> None:
        """Vuelve a pulsar 'Solicitar la baja' (pagina y dialogo) y espera el aviso de codigo enviado."""
        self.click_boton(self._boton_solicitar_baja)
        self.click_boton(self._boton_solicitar_baja)
        self.debe_ver(self._codigo_cancelacion_cuenta)

    def confirmar_baja(self, codigo: str) -> None:
        self.fill_box(self._codigo_verificacion_correo, codigo)
        self.click_boton(self._boton_confirmar_baja)
        self.debe_ver(self._baja_confirmada_mensaje, primero=True)

    def cancelar_baja(self) -> None:
        self.click_boton(self._boton_cancelar_baja)
        self.debe_ver(self._baja_cancelada)
