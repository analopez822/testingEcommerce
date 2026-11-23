from core.base_page import BasePage
from playwright.sync_api import Page, Locator, expect


class NavegacionPage(BasePage):
    """
        Barra de navegacion y menu de usuario, que casi todas las paginas usan.
        Los tests llaman a sus metodos (ir_a_login, ir_a_mi_cuenta...) en vez de buscar los botones a mano.
    """

    def __init__(self, page: Page): # constructor to create new instance of page, a new tab in browser
        super().__init__(page)      # calling constructor of parent class BasePage

        # locators
        self._inicio_boton: str = "Inicio"
        self._catalogo_boton: str = "Catálogo"
        self._novedades_boton: str = "Novedades"
        self._contraste_oscuro_boton: str = "Cambiar a tema claro"
        self._contraste_claro_boton: str = "Cambiar a tema oscuro"
        self._carrito_boton: str = "Abrir carrito"  # "/carrito"   #'[aria-label="Abrir carrito"]'
        self._login_boton: str = "Iniciar sesión"
        self._menu_usuario_boton: str = "Menú de usuario"
        self._mi_cuenta: str = "Mi cuenta"
        self._administracion: str = "Administración"
        self._configuracion: str = "Configuración"
        self._cerrar_sesion: str = "Cerrar sesión"

    def ir_a_login(self) -> None:
        self.buscar_por_rol("link", name=self._login_boton).click()

    def ir_al_catalogo(self) -> None:
        self.click_link(self._catalogo_boton)

    def abrir_carrito(self) -> None:
        self.buscar_por_rol("link", name=self._carrito_boton).click()

    def abrir_menu_usuario(self) -> None:
        self.click_boton(self._menu_usuario_boton)

    def opcion_menu(self, nombre: str) -> Locator:
        """Opcion del menu de usuario abierto (para comprobar si se ve o no segun el rol)."""
        return self.buscar_por_rol("menuitem", name=nombre)

    def comprobar_menu_usuario(self, visibles: list, ocultas: list = ()) -> None:
        """Abre el menu de usuario y comprueba que se ven unas opciones y otras no (segun el rol)."""
        self.abrir_menu_usuario()
        for nombre in visibles:
            expect(self.opcion_menu(nombre)).to_be_visible()
        for nombre in ocultas:
            expect(self.opcion_menu(nombre)).not_to_be_visible()

    def ir_a_mi_cuenta(self) -> None:
        self.abrir_menu_usuario()
        self.opcion_menu(self._mi_cuenta).click()

    def ir_a_administracion(self) -> None:
        self.abrir_menu_usuario()
        self.opcion_menu(self._administracion).click()

    def click_boton_contraste(self, status: str) -> None:
        if status == "Cambiar a tema claro":
            self.page.get_by_role("button", name=self._contraste_oscuro_boton).click()
        elif status == "Cambiar a tema oscuro":
            self.page.get_by_role("button", name=self._contraste_claro_boton).click()
