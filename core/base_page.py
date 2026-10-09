import os
import re
from playwright.sync_api import Page, Locator
from typing import List, Optional, Union, Any, Literal


class BasePage:
    """
        Clase base que envuelve las interacciones directas con PLaywright. Todas las clases de tipo Page Object deben
        heredar de esta clase.
        Si alguno de los metodos de Playwright cambia (nueva version, deprecated, etc) cambiarlos en esta clase
        es mas facil y rapido que cambiar todo el codigo
    """

    def __init__(self, page: Page):
        self.page : Page = page    # super().__init__(page)

        # global variables
        self._correo_super_admin: str = "superadmin@demo.com"
        self._contrasenia_super_admin: str = "ChangeMe!2026"
        self._correo_admin: str = "xxxxx"
        self._contrasenia_admin: str = "xxxxx"
        self._correo_usuario: str = "animiri@yahoo.es"
        self._contrasenia_usuario: str = "Mirianota8"
        self._contrasenia_incorrecta: str = "Incorrecta"


    def navegar(self, url: str = "http://localhost:5173/") -> None:
        self.page.goto(url, wait_until="networkidle")   # wait until page is loaded

    def encontrar(self, selector: str) -> Locator:
        """ Centraliza la busqueda de elementos que tienen id  """
        return self.page.locator(selector)

    def buscar_por_texto(self, texto: str) -> Locator:
        """ Centraliza la busqueda de elementos con text/role  """
        return self.page.get_by_text(texto)

    def buscar_por_placeholder(self, texto: str) -> Locator:
        return self.page.get_by_placeholder(texto)

    def buscar_por_rol(self, rol: str, name: str = None) -> Locator:
        return self.page.get_by_role(rol, name=name)

    def fill_box(self, locator: str, text: str) -> None:
        self.page.locator(locator).fill(text)

    def click_boton(self, button_text: str) -> None:
        """Click a button by its accessible name, waiting for it to be visible and scrolling it into view.
        Falls back to a force click if a normal click fails (covers overlays/obstructions).
        """
        # locator = self.page.get_by_role("button", name=re.compile(re.escape(button_text), re.IGNORECASE))
        # locator.click()
        self.page.get_by_role("button", name=button_text).click()

    def click_link(self, texto: str) -> None:
        self.page.click(f"a:has-text('{texto}')")
        # self.page.locator(f'a[href*="{texto}"]').click()

    def refresh_table(self):
        button = self.page.locator('button[aria-label="Actualizar lista"]')  # ==> CSS
        button.click()
        self.page.wait_for_timeout(3000)


    # def scroll_sideways(self, direction: str, pixels: int) -> None:
    #     """Scrolls the page horizontally by the specified number of pixels."""
    #     viewport = self.page.locator(".ag-body-horizontal-scroll-viewport")
    #     if direction == "right":
    #         viewport.evaluate(f"(el) => {{ el.scrollLeft += {pixels}; }}") # .evaluate and el.scrollLeft are javaScript
    #     elif direction == "left":
    #         viewport.evaluate(f"(el) => {{ el.scrollLeft -= {pixels}; }}")
    #
    # def resize_column(self, id: str, right: int, left: int):
    #     col_id = id
    #     header = self.page.locator(f'.ag-header-cell[col-id="{col_id}"]').first  #nth(0) # 1. Locate the resize handle element
    #     resize_hand = header.locator(".ag-header-cell-resize")  # barra separadora para arrastrar
    #     initial_box = header.bounding_box()                     # 2. Extract bounding box coordinates (x, y: width, height), todo el header, para obtener ancho inicial de la columna
    #     initial_width = initial_box["width"]
    #     print(f"Initial width: {initial_width}")
    #     handle_box = resize_hand.bounding_box()                 # Get the hand that will grab the resize handle
    #     start_x = handle_box["x"] + handle_box["width"] / 2     # 3. Calculate the center point of the resize handle
    #     start_y = handle_box["y"] + handle_box["height"] / 2
    #     print(f"Coordinadas iniciales: {start_x}, {start_y}")
    #     self.page.mouse.move(start_x, start_y)                  # 4. Hover over the element to reveal/activate it
    #     self.page.mouse.down()                                  # 5. Click and hold down the left mouse button
    #     self.page.mouse.move(start_x + right, start_y, steps=10)  # 6. Move the mouse to drag and resize
    #     self.page.mouse.up()                                    # 7. Release the mouse button
    #     current_box = header.bounding_box()
    #     assert current_box["width"] > initial_width
    #     # ahora disminuye el ancho de la columna, hay que obtener coordenadas siempre antes de volver a mover
    #     handle_box2 = resize_hand.bounding_box()
    #     final_box = header.bounding_box()
    #     final_width = final_box["width"]
    #     start_x2 = handle_box2["x"] + handle_box2["width"] / 2
    #     start_y2 = handle_box2["y"] + handle_box2["height"] / 2
    #     self.page.mouse.move(start_x2, start_y2)
    #     self.page.mouse.down()
    #     self.page.mouse.move(start_x2 - left, start_y2, steps=10)
    #     self.page.mouse.up()
    #     current_box = header.bounding_box()
    #     assert current_box["width"] < final_width
    #
    # def get_table_data(self,
    #         col_id: Optional[str] = None,
    #         return_count: bool = False
    # ) -> Union[int, List[Any]]:
    #     """
    #     Obtiene datos de AG Grid vía DOM.
    #
    #     - col_id=None -> todas las columnas; col_id="nombre" -> solo esa columna
    #     - return_count=True -> retorna la cantidad total de filas (usa aria-rowcount,
    #       confiable sin importar la virtualización, no requiere scroll)
    #     - return_count=False -> retorna un array con los datos (requiere scroll
    #       incremental para sortear la virtualización de AG Grid)
    #     """
    #     if return_count:
    #         grid = self.page.locator('.ag-root[role="grid"]')
    #         aria_row_count = int(grid.get_attribute("aria-rowcount"))
    #         return aria_row_count - 2  # resta filas de header (columnas + filtros)
    #
    #     viewport = self.page.locator(".ag-body-viewport")    ## ???
    #     collected = {}
    #
    #     def harvest():   # recursividad, puede consumir muchos recursos
    #         rows = self.page.locator(".ag-center-cols-container .ag-row").all() # fila por fila
    #         for row in rows:
    #             row_index = row.get_attribute("row-index")
    #             if row_index is None:  # when there's no more rows, the row-index attribute will be None, skip those rows
    #                 continue
    #             if col_id:
    #                 cell = row.locator(f'.ag-cell[col-id="{col_id}"]')
    #                 collected[row_index] = cell.inner_text() if cell.count() else None  # until there's no more cells
    #             else:
    #                 cells = row.locator(".ag-cell")
    #                 collected[row_index] = cells.all_inner_texts()
    #     harvest()
    #     prev_top = -1
    #     while True:     # javascript code to scroll the viewport and return new scroll position and max scroll position
    #         info = viewport.evaluate("""el => {
    #             const prevTop = el.scrollTop;
    #             el.scrollTop = el.scrollTop + el.clientHeight;
    #             return { newTop: el.scrollTop, maxTop: el.scrollHeight - el.clientHeight };
    #         }""")
    #         self.page.wait_for_timeout(150)
    #         harvest()
    #         if info["newTop"] == prev_top or info["newTop"] >= info["maxTop"]:
    #             break
    #         prev_top = info["newTop"]
    #     return [collected[k] for k in sorted(collected, key=int)]
    #
    #
    # def normalize_values(self, value: str | None):
    #     if value is None:
    #         return None
    #     text = value.strip()
    #     if text in ("", "-", "--"):
    #         return None
    #     map = {
    #         "Sí": True,
    #         "No": False,
    #         "True": True,
    #         "False": False,
    #         "Activo": True,
    #         "Inactivo": False
    #     }
    #     if text.lower() in map:
    #         return map[text.lower()]
    #     numeric_text = text.replace(",", "").replace(",", ".") if "," in text else text
    #     try:
    #         return float(numeric_text)
    #     except ValueError:
    #         pass
    #     return text.lower()
    #
    #
    # def verify_sorted(self, col_id: str, order: str = "asc", ignore: bool = True) -> bool:
    #     row_values = self.get_table_data(col_id=col_id)
    #     normalized = [self.normalize_values(v) for v in row_values]
    #     if ignore:
    #         normalized = [v for v in normalized if v is not None]
    #     if len(normalized) < 2:  # not enough data to determine sorting, because there's only headers' rows, not data rows
    #         return True
    #     reverse = order == "desc"
    #     expected = sorted(normalized, reverse=reverse)
    #     is_sorted = normalized == expected
    #     return is_sorted
    #
    #
    # def get_column(self, col_id: str):
    #     return self.page.locator(f".ag-header-cell[col-id='{col_id}']")
    #
    #
    # def drag_ag_column(self, source_col_id: str,
    #                    target_x: Optional[float]=None,
    #                    target_y: Optional[float]=None,
    #                    target_col_id: Optional[str]=None,
    #                    position: Literal["before", "after", "center"] = "after",
    #                    steps: int = 5):
    #     source_header = self.page.locator(f".ag-header-cell[col-id='{source_col_id}']").first
    #     source_box = source_header.bounding_box()
    #     start_x = source_box["x"] + source_box["width"] / 2
    #     start_y = source_box["y"] + source_box["height"] / 2
    #     if target_col_id:
    #         target_header = self.page.locator(f".ag-header-cell[col-id='{target_col_id}']").first
    #         target_box = target_header.bounding_box()
    #         if position == "before":
    #            end_x = target_box["x"] + 5
    #         elif position == "after":
    #             end_x = target_box["x"] + target_box["width"] - 5
    #         else:
    #             end_x = target_box["x"] + target_box["width"] / 2
    #         end_y = target_box["y"] + target_box["height"] / 2
    #     else:
    #         end_x, end_y = target_x, target_y
    #     self.page.mouse.move(start_x, start_y)
    #     self.page.mouse.down()
    #     for i in range(1, steps + 1):
    #         ix = start_x + (end_x - start_x) * i / steps
    #         iy = start_y + (end_y - start_y) * i / steps
    #         self.page.mouse.move(ix, iy)
    #         self.page.wait_for_timeout(15)
    #     self.page.mouse.up()
    #     self.page.wait_for_timeout(100)
    #
    #
    # def swap_ag_columns(self, col_id1: str, col_id2: str):
    #     self.drag_ag_column(source_col_id=col_id1, target_col_id=col_id2, position="after")
    #     self.page.wait_for_timeout(100)
    #     self.drag_ag_column(source_col_id=col_id2, target_col_id=col_id1, position="before")
    #     self.page.wait_for_timeout(100)
    #     self.drag_ag_column(source_col_id=col_id1, target_col_id=col_id2, position="after")
    #     self.page.wait_for_timeout(100)
    #
    #
    # def pin_ag_grid_column(self, col_id: str, position: Literal["left", "right"] = "left"):
    #     header = self.page.locator(f".ag-header-cell[col-id='{col_id}']").first
    #     header_box = header.bounding_box()
    #     grid_root = self.page.locator(".ag-root")
    #     root_box = grid_root.bounding_box()
    #     target_x = root_box["x"] + 5 if position == "left" else root_box["x"] + root_box["width"] - 5
    #     target_y = header_box["y"] + header_box["height"] / 2
    #     self.drag_ag_column(source_col_id=col_id, target_x=target_x, target_y=target_y)
    #     self.debug_pin_icon(col_id=col_id, side=position)
    #
    #
    # def debug_pin_icon(self, col_id: str, side: Literal["left", "right"] = "left",
    #                         hold_seconds: float = 2.5):
    #     """
    #     Arrastra la columna cerca del borde, mantiene el drag, y compara el DOM
    #     antes/después para detectar qué elemento nuevo aparece (el ícono de pin).
    #     Corré esto UNA VEZ para identificar el selector, no es para uso productivo.
    #     """
    #     header = self.page.locator(f'.ag-header-cell[col-id="{col_id}"]').first
    #     header_box = header.bounding_box()
    #     header_viewport = self.page.locator(".ag-header-viewport")
    #     viewport_box = header_viewport.bounding_box()
    #
    #     start_x = header_box["x"] + header_box["width"] / 2
    #     start_y = header_box["y"] + header_box["height"] / 2
    #
    #     # Cerca del borde pero SIN salir del todo (ajustá este offset si activa el hide)
    #     target_x = viewport_box["x"] + 10 if side == "left" else viewport_box["x"] + viewport_box["width"] - 10
    #     target_y = start_y
    #
    #     # Snapshot del DOM antes
    #     before = set(self.page.evaluate("""() =>
    #         Array.from(document.querySelectorAll('*'))
    #             .map(el => el.className + '|' + el.tagName)
    #     """))
    #
    #     self.page.mouse.move(start_x, start_y)
    #     self.page.mouse.down()
    #     steps = 20
    #     for i in range(1, steps + 1):
    #         ix = start_x + (target_x - start_x) * i / steps
    #         self.page.mouse.move(ix, target_y)
    #         self.page.wait_for_timeout(15)
    #
    #     self.page.wait_for_timeout(hold_seconds * 1000)  # mantener el hold
    #
    #     # Snapshot del DOM durante el hold (con el mouse aún abajo)
    #     after = set(self.page.evaluate("""() =>
    #         Array.from(document.querySelectorAll('*'))
    #             .map(el => el.className + '|' + el.tagName)
    #     """))
    #
    #     new_elements = after - before
    #     print("Elementos nuevos aparecidos durante el hold:")
    #     for el in new_elements:
    #         print(" -", el)
    #
    #     self.page.mouse.up()
    #
    #
    # def hide_ag_grid_column(self, col_id: str):
    #     header = self.page.locator(f".ag-header-cell[col-id='{col_id}']").first
    #     header_box = header.bounding_box()
    #     target_x = header_box["x"] + header_box["width"] / 2
    #     target_y = header_box["y"] - 300
    #     self.drag_ag_column(source_col_id=col_id, target_x=target_x, target_y=target_y)


    def debugger(self):
        if os.environ.get("DEBUG_PAUSA")=="1":
            self.page.pause()
