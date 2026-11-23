"""
Pruebas del PROPIO framework (no de la tienda): usan paginas HTML de mentira con `page.set_content`,
asi que funcionan sin la tienda levantada. Sirven para comprobar que config, pages y componentes
hacen lo que dicen, y como ejemplo de uso de cada pieza.
"""
import pytest
from playwright.sync_api import expect

from components.ag_grid import AgGrid
from components.chat import ChatDialogo
from components.lista_tarjetas import ListaTarjetas, SELECTOR_REJILLA
from core import config
from datos.prueba import DIRECCION, DIRECCION_EDITADA
from pages.aplicacion import Aplicacion


class TestConfig:
    def test_usuario_por_rol(self):
        for rol in config.ROLES:
            u = config.usuario(rol)
            assert u.rol == rol and u.email and u.contrasenia

    def test_rol_desconocido(self):
        with pytest.raises(ValueError, match="Rol desconocido"):
            config.usuario("invitado")

    def test_falta_variable(self, monkeypatch):
        monkeypatch.delenv("ADMIN_PASSWORD")
        with pytest.raises(RuntimeError, match="ADMIN_PASSWORD"):
            config.usuario("admin")


class TestAplicacion:
    def test_cada_page_se_crea_una_vez_y_comparte_ventana(self, app: Aplicacion):
        assert app.login is app.login
        assert app.login.page is app.page is app.mi_cuenta.pedidos.page


class TestLoginYNavegacion:
    PAGINA = """
      <nav><a href="#">Iniciar sesión</a><button>Entrar</button></nav>
      <form>
        <input name="email"><input name="password">
        <button type="button" onclick="document.body.insertAdjacentHTML('beforeend', '<p>Hola de nuevo, Ana</p>')">Entrar</button>
        <button type="button">Entrar con llave de acceso</button>
        <input type="checkbox" aria-label="Mantener la sesión en este dispositivo">
      </form>"""

    def test_iniciar_sesion_rellena_y_pulsa_el_entrar_del_formulario(self, app: Aplicacion):
        app.page.set_content(self.PAGINA)
        usuario = config.usuario("customer")
        app.login.iniciar_sesion(usuario)     # incluye comprobar el toast 'Hola de nuevo, '
        assert app.page.input_value("input[name='email']") == usuario.email
        assert app.page.input_value("input[name='password']") == usuario.contrasenia

    def test_alternar_mantener_sesion(self, app: Aplicacion):
        app.page.set_content(self.PAGINA)
        casilla = app.page.get_by_role("checkbox")
        app.login.alternar_mantener_sesion()
        expect(casilla).to_be_checked()
        app.login.alternar_mantener_sesion()
        expect(casilla).not_to_be_checked()

    def test_menu_usuario_visibles_y_ocultas(self, app: Aplicacion):
        app.page.set_content("""
          <button onclick="document.getElementById('m').hidden=false">Menú de usuario</button>
          <div id="m" hidden><div role="menuitem">Mi cuenta</div><div role="menuitem">Cerrar sesión</div></div>""")
        nav = app.navegacion
        nav.comprobar_menu_usuario(visibles=[nav._mi_cuenta, nav._cerrar_sesion], ocultas=[nav._administracion])

    def test_menu_usuario_falla_si_falta_una_opcion_visible(self, app: Aplicacion):
        app.page.set_content("""
          <button onclick="document.getElementById('m').hidden=false">Menú de usuario</button>
          <div id="m" hidden><div role="menuitem">Mi cuenta</div></div>""")
        with pytest.raises(AssertionError):
            app.navegacion.comprobar_menu_usuario(visibles=["Administración"])

    def test_ir_a_mi_cuenta(self, app: Aplicacion):
        app.page.set_content("""
          <button onclick="document.getElementById('m').hidden=false">Menú de usuario</button>
          <div id="m" hidden><div role="menuitem" onclick="document.title='en mi cuenta'">Mi cuenta</div></div>""")
        app.navegacion.ir_a_mi_cuenta()
        assert app.page.title() == "en mi cuenta"


class TestComponentes:
    def test_debe_ver_y_no_debe_ver(self, app: Aplicacion):
        app.page.set_content("<p>Dirección guardada</p>")
        app.login.debe_ver("Dirección guardada")
        app.login.no_debe_ver("Otra cosa")
        with pytest.raises(AssertionError):
            app.login.debe_ver("Otra cosa", primero=True)

    def test_lista_tarjetas_describe(self, app: Aplicacion, capsys):
        app.page.set_content("<ul class='flex flex-col gap-3'><li>Pedido A</li><li>Pedido B</li></ul>")
        lista = ListaTarjetas(app.page)
        lista.describir("pedidos", "Informacion del pedido")
        salida = capsys.readouterr().out
        assert "Numero total de pedidos: 2" in salida and "Informacion del pedido: Pedido B" in salida

    def test_lista_tarjetas_vacia_y_rejilla(self, app: Aplicacion, capsys):
        app.page.set_content("<ul class='grid gap-4 md:grid-cols-2'></ul>")
        ListaTarjetas(app.page, SELECTOR_REJILLA).describir("direcciones", "Direccion")
        assert "No existen direcciones" in capsys.readouterr().out

    def test_chat_enviar_y_ultimo_mensaje(self, app: Aplicacion):
        app.page.set_content("""
          <button onclick="document.getElementById('c').hidden=false">Abrir el chat</button>
          <section id="c" hidden role="dialog"><h2>Chat con la tienda</h2>
            <ul class="flex flex-col gap-3"></ul>
            <input placeholder="Escribe tu mensaje">
            <button onclick="const i=document.querySelector('input'); document.querySelector('ul').insertAdjacentHTML('beforeend','<li>'+i.value+'</li>')">Enviar</button>
          </section>""")
        chat = ChatDialogo(app.page)
        chat.abrir()
        chat.enviar("hola")
        chat.enviar("adios")
        chat.debe_mostrar("hola")
        expect(chat.ultimo_mensaje()).to_have_text("adios")

    def test_chat_abrir_conversacion_admin(self, app: Aplicacion):
        app.page.set_content("""
          <button class="flex flex-col gap-0.5">Luis</button>
          <button class="flex flex-col gap-0.5" onclick="document.title='Ana abierta'">Ana Redondo</button>""")
        ChatDialogo(app.page).abrir_conversacion_con("Ana")
        assert app.page.title() == "Ana abierta"

    def test_ag_grid_accion_en_fila(self, app: Aplicacion):
        app.page.set_content("""
          <div role="row" aria-label="P-1 Luis"><button aria-label="Acciones" onclick="m1.hidden=false">...</button></div>
          <div role="row" aria-label="P-2 Ana"><button aria-label="Acciones" onclick="m2.hidden=false">...</button></div>
          <div id="m1" hidden><div role="menuitem" onclick="document.title='luis'">Aprobar</div></div>
          <div id="m2" hidden><div role="menuitem" onclick="document.title='ana'">Aprobar</div></div>""")
        AgGrid(app.page).accion_en_fila("P-2 Ana", "Aprobar")
        assert app.page.title() == "ana"


class TestFormularioDireccion:
    """Replica los selectores del formulario de 'Finalizar compra' para comprobar el orden y los datos."""
    FORMULARIO = """
      <input name="fullName"><button role="combobox">Pais</button><button role="combobox" onclick="ciudades.hidden=false">Ciudad</button>
      <input placeholder="Buscar ciudad"><ul id="ciudades" hidden class="max-h-64 overflow-y-auto p-1"><li><button>Madrid</button></li></ul>
      <input id="street"><input name="postalCode"><input name="province"><input name="phone"><textarea name="notes"></textarea>
      <button onclick="document.body.insertAdjacentHTML('beforeend','<p>Dirección guardada</p><p>Dirección actualizada</p>')">Guardar dirección</button>
      %s"""

    def _valores(self, page):
        return {n: page.input_value(s) for n, s in {
            "nombre": "input[name='fullName']", "calle": "#street", "cp": "input[name='postalCode']",
            "provincia": "input[name='province']", "telefono": "input[name='phone']", "notas": "textarea",
        }.items()}

    def test_rellenar_direccion(self, app: Aplicacion):
        app.page.set_content(self.FORMULARIO % "")
        app.finalizar_compra.rellenar_direccion(DIRECCION)
        assert self._valores(app.page) == {
            "nombre": DIRECCION.nombre, "calle": DIRECCION.calle, "cp": DIRECCION.codigo_postal,
            "provincia": DIRECCION.provincia, "telefono": DIRECCION.telefono, "notas": DIRECCION.notas}

    def test_cargar_direccion_pulsa_usar_otra_si_hay_guardadas(self, app: Aplicacion):
        app.page.set_content(self.FORMULARIO % "<h3>Tus direcciones</h3><button onclick=\"document.title='otra'\">Usar otra dirección</button>")
        app.finalizar_compra.cargar_direccion(DIRECCION)
        assert app.page.title() == "otra"

    def test_cargar_direccion_sin_guardadas_no_pulsa_nada(self, app: Aplicacion):
        app.page.set_content(self.FORMULARIO % "")
        app.finalizar_compra.cargar_direccion(DIRECCION)
        assert app.page.title() == ""

    def test_editar_contacto_solo_toca_provincia_telefono_y_notas(self, app: Aplicacion):
        app.page.set_content(self.FORMULARIO % "")
        app.finalizar_compra.editar_contacto(DIRECCION_EDITADA)
        valores = self._valores(app.page)
        assert valores["provincia"] == "Barcelona" and valores["calle"] == ""
