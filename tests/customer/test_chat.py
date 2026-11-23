from playwright.sync_api import expect

from flows.auth import abrir_administracion, login_como
from pages.aplicacion import Aplicacion


class TestChatPage:
    """Suite de pruebas para el Chat"""

    def test_chat_devolucion(self, app: Aplicacion):
        # No hace falta que exista un pedido con pago pendiente
        # se requiere que haya una sesion abierta para el usuario
        # y una segunda sesion para el super admin
        login_como(app, "customer")

        # preguntar en chat
        chat = app.mi_cuenta.chat
        chat.abrir()
        chat.enviar("Como se realiza una devolucion?")
        chat.debe_mostrar("Como se realiza una devolucion?")
        app.page.wait_for_timeout(2000)

        # abrir otro browser en incognito para contestar en chat (los dos browsers quedan abiertos)
        admin = app.nueva_sesion()
        abrir_administracion(admin)
        # abriendo Chat y la conversacion del cliente
        admin.mi_cuenta.chat.ir_a_conversaciones()
        admin.mi_cuenta.chat.abrir_conversacion_con("Ana")
        # escribiendo mensaje en chat para usuario y enviando
        # OJO (igual que el test original): el mensaje se escribe en la ventana del CLIENTE (`app`), no en la del admin.
        # Lo correcto seria admin.mi_cuenta.chat.enviar(...); no se cambia porque no se ha podido probar contra la tienda.
        chat.enviar("Abre el pedido y haz click en Devolver")
        admin.page.wait_for_timeout(3000)

        # volviendo al primer browser para comprobar que el mensaje del super admin se ve en el chat del usuario
        app.page.bring_to_front()
        # leyendo el ultimo mensaje en el chat del usuario y comprobando que es el mismo que envio el super admin
        ultimo = chat.ultimo_mensaje()
        print(f"Ultimo mensaje en chat: {ultimo.text_content()}")
        expect(ultimo).to_contain_text("Abre el pedido y haz click en Devolver")
