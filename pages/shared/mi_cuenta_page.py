from core.base_page import BasePage
from playwright.sync_api import Page

class MiCuentaPage(BasePage):
    """
        Clase con los locators y metodos de Mi Cuenta
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators Mi Cuenta
        self._datos_personales: str = "Datos personales"
        self._telefono: str = "input[name='phone']"
        self._nuevo_email: str = "input[name='newEmail']"
        self._nueva_contrasenia: str = "input[name='password']"
        self._boton_guardar_cambios: str = "Guardar cambios"
        self._correo: str = "Correo electrónico"
        self._boton_correo: str = "Cambiar email"
        self._descargar_datos: str = "Descargar mis datos"
        self._boton_descargar_datos: str = "Descargar JSON"
        self._eliminar_cuenta: str = "Eliminar mi cuenta"
        self._boton_solicitar_baja: str = "Solicitar la baja"
        self._datos_actualizados: str = "Datos actualizados"
        self._email_con_codigo_enviado: str = "Te hemos enviado un código a "
        self._email_actualizado = str =  "Email actualizado"
        self._codigo_verificacion_correo = str = "input[autocomplete='one-time-code'][data-slot='input-otp']"
        self._boton_confirmar: str = "Confirmar"
        self._boton_descargar_json: str = "Descargar JSON"
        self._porque_te_vas: str =  "textarea[data-slot='textarea'][name='reason']"

        # locator dialogo cancelar cuenta
        self._cancelar_cuenta: str = "Solicitar la baja de tu cuenta"
        self._boton_cancelar: str = "Cancelar"
        self._codigo_cancelacion_cuenta: str = "Te hemos enviado un código para "
        self._boton_confirmar_baja: str = "Confirmar la baja"
        self._baja_confirmada_mensaje: str = "Tu cuenta se eliminará "
        self._boton_cancelar_baja: str = "Cancelar la baja"
        self._baja_cancelada: str = "Hemos cancelado la baja de tu cuenta"

        # locators panel izquierdo
        self._mis_datos: str = "Mis datos"
        self._texto_mis_datos: str = "Tu información personal y cómo entras en la tienda."
        self._mis_pedidos: str = "Mis pedidos"
        self._direcciones: str = "Direcciones"
        self._metodos_pago: str = 'Métodos de pago'
        self._devoluciones: str = 'Devoluciones'
        self._chat: str = 'Chat'
        self._suscripcion: str = 'Suscripción'
        self._juega_gana: str = 'Juega y gana'
        self._seguridad: str = 'Seguridad'
        self._soporte: str = 'Soporte'

        # locators para Mis Pedidos
        self._pedidos_header: str = 'Aquí tienes todo lo que has comprado.'
        self._boton_ver_detalle: str = "Ver detalle"
        self._link_volver_a_pedidos: str = "Volver a mis pedidos"
        self._boton_cancelar_pedido: str = "Cancelar pedido"
        self._dialogo_cancelar_pedido: str = "¿Cancelar el pedido "
        self._confirmacion_pedido_cancelado: str = " cancelado"
        self._boton_descargar_recibo: str = "Descargar recibo"
        self._boton_chat: str = "Abrir el chat"  #"button[aria-label='Abrir el chat']"
        self._dialogo_chat_con_tienda: str = "Chat con la tienda"
        self._caja_mensaje_chat: str = "Escribe tu mensaje"
        self._boton_enviar_chat: str = "Enviar"   #"button[data-slot='button'][aria-label='Enviar']"
        self._boton_pago_prueba: str = "Pago de prueba"
        self._dialogo_pago_prueba: str = "Esta pantalla imita a la pasarela real: elige el resultado y vuelve a la tienda."
        self._boton_pago_correcto: str = "Simular pago correcto"
        self._pago_completado: str = "Pago completado"
        self._boton_pagar_tajeta_apple_google: str = "Tarjeta, Apple Pay o Google Pay"
        self._boton_devolver_pedido: str = "Devolver"
        self._dialogo_devolver_pedido: str = "Cuéntanos qué ha pasado. Revisaremos la solicitud y te diremos cómo enviarlo."
        self._motivo_devolucion: str = "textarea[name='reason']"

        # locators para Direcciones
        self._direcciones_header: str = 'Las que te proponemos al finalizar la compra.'
        self._boton_eliminar: str =  "Eliminar"
        self._dialogo_eliminar: str = "Eliminar dirección"
        self._confirmacion_direccion_eliminada: str = "Dirección eliminada"
        self._boton_editar: str = "Editar"
        self._dialogo_editar: str = "Solo enviamos a países de la Unión Europea."
        self._boton_enviar_solicitud: str = "Enviar solicitud"
        self._confirmacion_solicitud_devolucion: str = "Solicitud enviada"
        self._no_mas_devoluciones: str = "Este pedido ya no admite devoluciones."


        # locators para Devoluciones
        self._devoluciones_usuario_header: str = 'Lo que has pedido devolver y en qué punto está.'
        self._devoluciones_superadmin_header: str = 'Solicitudes de los clientes y su resolución.'
        self._dialogo_aprobar_devolucion: str = "Mensaje para el cliente"
        self._devolucion_aprobada: str = "Devolución aprobada"
        self._dialogo_reembolso: str = "Devolución del pedido "
        self._stock_repuesto: str = "Recibida: stock repuesto"
        self._boton_reembolsar: str = "Reembolsar"
        self._dialogo_confirmar_reembolso: str = "Reembolsar la devolución"
        self._caja_aprobar_devolucion: str = "textarea[name='note']"
        self._boton_aprobar_devolucion: str = "Aprobar"
        self._dialogo_reembolso: str = "Por defecto se devuelve el precio de las unidades menos la comisión de la política."
        self._reembolso_confirmado: str = "Reembolso enviado"
        self._dialogo_reembolso2: str = "Reembolsar la devolución"
        self._toast_confirmacion_reembolso: str = "Reembolso enviado"

        # locators para chat
        self._boton_chat_usuario: str = "button[class*='flex flex-col gap-0.5']" # "[data-slot='card-content'] button"
        self._mensajes_en_chat: str = "section[role='dialog'][aria-label='Chat con la tienda']"