from core.base_page import BasePage
from playwright.sync_api import Page, expect

class LoginPage(BasePage):
    """
        Clase con los locators y metodos de login
    """

    def __init__(self, page: Page):
        super().__init__(page)

        # locators pagina login
        self._texto: str = "Accede a tu cuenta para comprar y seguir tus pedidos."
        self._email: str = "Email"  # input id   data-slot="input2"
        self._password: str = "Contraseña"  # input id   data-slot="input2"
        self._boton_ocultar_contrasenia: str = "Ocultar contraseña"
        self._boton_contrasenia: str = "Mostrar contraseña"


    def click_boton_contrasenia(self, status: str) -> None:
        if status == "Mostrar contraseña":
            self.page.get_by_role("button", name=self._boton_contrasenia).click()
        elif status == "Ocultar contraseña":
            self.page.get_by_role("button", name=self._boton_ocultar_contrasenia).click()

    def login(self, email: str, password: str) -> None:
        self.navegar("http://localhost:5173/")
        expect(self.buscar_por_texto("Bienvenido a Test Shop")).to_be_visible()  # toast



