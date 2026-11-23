"""
Vocabulario comun: textos y selectores que aparecen en MAS DE UNA pagina.

Regla de oro: si un boton, campo o mensaje sale en dos sitios, vive aqui UNA sola vez y las
pages lo importan. Si solo existe en una pantalla, se queda como atributo de esa page.
Asi, cuando la tienda cambie "Cancelar" por "Cerrar", se toca una linea y no cinco.
"""


class Campo:
    """Selectores CSS de campos de formulario que se repiten."""
    EMAIL = "input[name='email']"
    PASSWORD = "input[name='password']"
    TELEFONO = "input[name='phone']"
    MOTIVO = "textarea[name='reason']"          # baja de cuenta y devolucion de pedido
    CODIGO_OTP = "input[autocomplete='one-time-code']"


class Boton:
    """Nombres accesibles de botones/enlaces que se repiten."""
    CANCELAR = "Cancelar"
    ELIMINAR = "Eliminar"
    DESCARGAR_JSON = "Descargar JSON"
    FINALIZAR_COMPRA = "Finalizar compra"
    PAGAR_CON_TARJETA = "Tarjeta, Apple Pay o Google Pay"
    CREAR_CUENTA = "Crear cuenta"
    VOLVER_A_INICIAR_SESION = "Volver a iniciar sesión"


class Mensaje:
    """Mensajes (toasts / avisos) que se repiten."""
    DEMASIADOS_INTENTOS = "Demasiados intentos. Inténtalo más tarde."


class Panel:
    """Enlaces del panel izquierdo de 'Mi cuenta' (y de Administracion para Chat y Devoluciones)."""
    MIS_DATOS = "Mis datos"
    MIS_PEDIDOS = "Mis pedidos"
    DIRECCIONES = "Direcciones"
    METODOS_PAGO = "Métodos de pago"
    DEVOLUCIONES = "Devoluciones"
    CHAT = "Chat"
    SUSCRIPCION = "Suscripción"
    JUEGA_Y_GANA = "Juega y gana"
    SEGURIDAD = "Seguridad"
    SOPORTE = "Soporte"

    # orden en el que aparecen en pantalla, sin Chat (que tiene su propio componente)
    CUENTA_CLIENTE = (MIS_DATOS, MIS_PEDIDOS, DIRECCIONES, METODOS_PAGO, DEVOLUCIONES,
                      SUSCRIPCION, JUEGA_Y_GANA, SEGURIDAD, SOPORTE)
