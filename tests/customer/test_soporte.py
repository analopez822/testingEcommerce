import re

from playwright.sync_api import expect

from conftest import app_login, app_navegacion, app_mi_cuenta
from pages.shared.login_page import LoginPage
from pages.shared.navegacion_page import NavegacionPage
from pages.shared.mi_cuenta_page import MiCuentaPage


class TestSoportePage:
    """Suite de pruebas para la pagina Soporte, que es la ultima seccion del panel izquierdo de Mi Cuenta"""

    def login(self, app_login: LoginPage, app_navegacion: NavegacionPage, correo: str, contrasenia: str):
        # esta funcion deberia estar centralizada, maybe en base_page.py?
        # funcion para login, con las credenciales que se pasen en parametros
        app_login.navegar()
        app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
        expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
        app_login.fill_box(app_login._email, correo)
        app_login.fill_box(app_login._password, contrasenia)
        app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
        toast = app_login.buscar_por_texto(app_login._login_exito)
        expect(toast).to_be_visible()

    def lista_soporte(self, app_mi_cuenta: MiCuentaPage):
        # esta funcion deberia estar centralizada, maybe en base_page.py?
        # contando items en lista Soporte y comprobando que no esta vacia.
        # extrae IDs de consultas. Devuelve el id de la ultima consulta.
        # Puede valer para devoluciones alterando la linea de match
        lista_soporte = app_mi_cuenta.encontrar(app_mi_cuenta._lista_soporte)   # CSS selector "ul[class='flex flex-col gap-3'] > li"
        consultas = lista_soporte.count()
        consulta_ids = []   # creating empty list to save consultas' ids

        if consultas > 0:
            print("Existen consultas.")
            print(f"Numero total de consultas: {consultas}")
            # Iterando sobre todos los elementos y extrayendo asunto consulta
            # .all() resolves the locator to an array of individual element locators
            for item in lista_soporte.all(): # sin .all() el código fallará con un error, xk un objeto Locator en Playwright no es iterable directamente
                text = item.text_content()
                print(f"Consulta: {text}")
                # extrayendo el ID de la consulta del texto ('T-2026-1225')
                match = re.search(r"T-\d{4}-\d+", text)  # Para devoluciones ==> re.search(r"P-\d{4}-\d+", text)
                if match:
                    consulta_ids.append(match.group(0))  # group(0) & group() return whole match
            print(consulta_ids)
        else:
            print("No existen consultas en Soporte")

        ticket = consulta_ids[0] if consulta_ids else None   # la parte del if es para cuando la lista este vacia
        return ticket

    def test_soporte(self, app_login: LoginPage, app_navegacion: NavegacionPage, app_mi_cuenta: MiCuentaPage):
        # app_login.debugger()
        # test para crear una nueva consulta como usuario y luego responderla como super admin
        # logging como usuario
        self.login(app_login, app_navegacion, app_login._correo_usuario, app_login._contrasenia_usuario)
        # click en menu usuario y luego Mi Cuenta
        app_navegacion.click_boton(app_navegacion._menu_usuario_boton)
        app_navegacion.buscar_por_rol("menuitem", name=app_navegacion._mi_cuenta).click()
        # entrando en soporte y comprobando titulo
        app_mi_cuenta.click_link(app_mi_cuenta._soporte)
        expect(app_mi_cuenta.buscar_por_rol("heading", name=app_mi_cuenta._soporte, exact=True)).to_be_visible()
        # creando nueva consulta
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_nueva_consulta)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._dialogo_nueva_consulta)).to_be_visible()
        app_mi_cuenta.fill_box(app_mi_cuenta._asunto_box, "Gafas sin patillas")     ######
        app_mi_cuenta.fill_box(app_mi_cuenta._cuentanos_box, "Me gustaría saber devolver estas gafas.")
        app_mi_cuenta.click_boton(app_mi_cuenta._enviar_consulta_boton)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._consulta_enviada_mensaje)).to_be_visible()
        # comprobando que la consulta se ve en la lista de consultas: refrescando la pagina y contando items en lista Soporte
        app_mi_cuenta.page.reload()
        app_mi_cuenta.page.wait_for_timeout(2000)  # Hace falta!! Si no, no ve la lista despues del refresh
        ticket = self.lista_soporte(app_mi_cuenta)
        print(ticket)
        lista_soporte = app_mi_cuenta.encontrar(app_mi_cuenta._lista_soporte).first
        expect(lista_soporte).to_contain_text(f"{ticket}")
        app_mi_cuenta.page.wait_for_timeout(3000)

        # abriendo otro browser en incognito para contestar la consulta como super admin
        browser2 = app_navegacion.abrir_ventana_incognito(close_original_page=False) # para testear chat con los dos browsers abiertos
        admin_navegacion = NavegacionPage(browser2)    # pasando nuevo contexto a clases involucradas en test
        admin_login = LoginPage(browser2)
        admin_mi_cuenta = MiCuentaPage(browser2)
        admin_login.navegar()    #
        admin_navegacion.buscar_por_rol("link", name=admin_navegacion._login_boton).click()
        expect(admin_login.buscar_por_texto(admin_login._texto)).to_be_visible()
        admin_login.fill_box(admin_login._email, admin_mi_cuenta._correo_super_admin)
        admin_login.fill_box(admin_login._password, admin_login._contrasenia_super_admin)
        admin_login.buscar_por_rol("button", name=admin_login._boton_entrar).nth(1).click()
        toast = admin_login.buscar_por_texto(admin_login._login_exito)
        expect(toast).to_be_visible()
        admin_navegacion.click_boton(admin_navegacion._menu_usuario_boton)
        admin_navegacion.buscar_por_rol("menuitem", name=admin_navegacion._administracion).click()
        # abriendo Tickets, comprobando header y luego abriendo la consulta del usuario
        # no hace falta refresh page porque acabamos de logear como super admin y la lista de consultas se carga automaticamente
        admin_mi_cuenta.click_link(admin_mi_cuenta._tickets)
        expect(admin_mi_cuenta.buscar_por_rol("heading", name=admin_mi_cuenta._tickets)).to_be_visible()

        # iterando sobre las consultas, hasta encontrar la que contiene el ticket id de la linea 73
        # y hacer click para abrir y responder. Hace scroll hasta el fondo de la pantalla, y click en boton siguiente, si es necesario

        # ticket_soporte = app_mi_cuenta.page.locator(".ag-grid-scrolling-rows[role='gridcell'][col-id='number']").filter(has_text="T-2026-1220")
        # ticket_soporte.click()

        # rows = app_mi_cuenta.page.locator('.ag-grid-scrolling-rows [role="row"]').all()
        # for row in rows:
        #     number_cell = row.locator('[role="gridcell"][col-id="number"]')
        #     if number_cell.inner_text().strip() == ticket:
        #         number_cell.click()  # Or row.click()
        #         break

        viewport = admin_mi_cuenta.page.locator(".ag-grid-viewport")   # toda la tabla, incluyendo header
        target_cell = admin_mi_cuenta.page.locator(
            '.ag-grid-scrolling-rows [role="gridcell"][col-id="number"]', has_text=ticket)
        next_page_btn = admin_mi_cuenta.page.locator('[data-ref="btNext"]')

        # Ensure the grid has loaded at least one row before starting
        admin_mi_cuenta.page.locator('.ag-grid-scrolling-rows [role="row"]').first.wait_for()
        previous_scroll_top = -1    # creates a starting marker used to detect when the scrollbar hits the very bottom of the table.

        while True:
            # Check if the target row is currently rendered in the DOM
            if target_cell.count() > 0:
                target_cell.first.scroll_into_view_if_needed()
                target_cell.first.click()
                break   # break exits only the current loop, while return exits the entire function immediately.
                        # Playwright locator methods: .count() returns an integer showing how many elements match a locator,
                        # while .all() returns a Python list containing individual Locator objects

            # Check if we have reached the very bottom of the current 20-row page
            current_scroll_top = viewport.evaluate("el => el.scrollTop")
            if current_scroll_top == previous_scroll_top:

                # Check if AG Grid has NOT added the 'ag-disabled' class to the Next button (last screen)
                btn_classes = next_page_btn.get_attribute("class") or ""
                if "ag-disabled" not in btn_classes:
                    next_page_btn.click()
                    admin_mi_cuenta.page.wait_for_timeout(300)  # Wait for the new 20 rows to load
                    previous_scroll_top = -1  # Reset scroll tracker for the new page
                    continue  # Restart the loop to scan the new page from the top

                # If 'ag-disabled' IS present, we are on the final page
                raise ValueError(f"Row with number '{ticket}' was not found in any page of the table.")
            previous_scroll_top = current_scroll_top

            # Scroll down by 80% of the viewport's visible height
            viewport.evaluate("el => el.scrollTop += el.clientHeight * 0.8")
            admin_mi_cuenta.page.wait_for_timeout(150)   # pause to let AG Grid render the newly exposed rows

        expect(admin_mi_cuenta.buscar_por_texto(f"{ticket}").first).to_be_visible()
        expect(admin_mi_cuenta.buscar_por_texto("Abierta").first).to_be_visible()
        admin_mi_cuenta.debugger()
        admin_mi_cuenta.encontrar(admin_mi_cuenta._estado_dropdown).click()
        # admin_mi_cuenta.buscar_por_rol("combobox", name="Cambiar estado").click()
        # admin_mi_cuenta.buscar_por_texto("En curso").nth(2).click()
        admin_mi_cuenta.page.get_by_label("En curso").get_by_text("En curso").click()    ############
        admin_mi_cuenta.encontrar(admin_mi_cuenta._priority_dropdown).click()
        admin_mi_cuenta.page.get_by_text("Alta", exact=True).click()         #############
        admin_mi_cuenta.fill_box(admin_mi_cuenta._respuesta_soporte, "Sin ningun problema")
        admin_mi_cuenta.click_boton(admin_mi_cuenta._boton_responder_cliente)
        expect(admin_mi_cuenta.buscar_por_texto(admin_mi_cuenta._respuesta_enviada_toast)).to_be_visible()
        # cerrando dialogo soporte
        admin_mi_cuenta.encontrar(admin_mi_cuenta._boton_close).click()
        expect(admin_mi_cuenta.buscar_por_texto("Cambiar estado")).not_to_be_visible()


        # volviendo al primer browser para comprobar que el mensaje del super admin se ve en el chat del usuario
        app_mi_cuenta.page.bring_to_front()
        app_mi_cuenta.page.reload()
        # verifica que en fila con ticket id aparece 'Te hemos contestado'
        lista_soporte = app_mi_cuenta.encontrar(app_mi_cuenta._lista_soporte).first
        expect(lista_soporte).to_contain_text(f"{ticket}")
        expect(lista_soporte).to_contain_text("Te hemos contestado")
        # abre consulta, verifica respuesta admin y click 'Dar por resuelta'
        lista_soporte.click()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_dar_por_resuelta)
        # verificar dialogo de resolver consulta y click 'Dar por resuelta' otra vez
        expect(app_mi_cuenta.buscar_por_texto("¿Dar la consulta por resuelta?")).to_be_visible()
        app_mi_cuenta.click_boton(app_mi_cuenta._boton_dar_por_resuelta)
        expect(app_mi_cuenta.buscar_por_texto(app_mi_cuenta._consulta_cerrada_confirmacion)).to_be_visible()

        app_login.page.wait_for_timeout(3000)