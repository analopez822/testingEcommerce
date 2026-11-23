from playwright.sync_api import Page, Locator

# Mis pedidos, Devoluciones y los mensajes del chat usan la misma lista; Direcciones usa una rejilla
SELECTOR_LISTA = "ul[class='flex flex-col gap-3'] > li"
SELECTOR_REJILLA = "ul[class='grid gap-4 md:grid-cols-2'] > li"


class ListaTarjetas:
    """Lista de tarjetas de la cuenta (pedidos, devoluciones, direcciones, mensajes del chat)."""

    def __init__(self, page: Page, selector: str = SELECTOR_LISTA):
        self.items: Locator = page.locator(selector)

    def contar(self) -> int:
        return self.items.count()

    def describir(self, plural: str, etiqueta_item: str) -> None:
        """Imprime cuantos elementos hay y el texto de cada uno. Ej: describir("pedidos", "Informacion del pedido")"""
        total = self.contar()
        if total == 0:
            print(f"No existen {plural}")
            return
        print(f"Existen {plural}")
        print(f"Numero total de {plural}: {total}")
        for item in self.items.all():     # .all() convierte el locator en una lista de locators, uno por elemento
            print(f"{etiqueta_item}: {item.text_content()}")
