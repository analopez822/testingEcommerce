# Guía del framework (explicada paso a paso)

Esta guía explica **cómo está organizado el framework de pruebas y cómo añadir cosas nuevas sin repetirte**.
Los trozos de código de esta guía son **ejemplos para entender**; no están en el proyecto salvo que se diga lo contrario.

---

## 1. La idea en una frase

> **Cada cosa se escribe una sola vez y vive en un solo sitio. Los tests solo dicen _qué_ quieren hacer, nunca _cómo_.**

Piensa en un restaurante:

| En el restaurante | En el framework | Qué hace |
|---|---|---|
| El **cliente** pide "una pizza" | El **test** | Dice qué quiere: `app.login.iniciar_sesion(...)` |
| El **camarero** | La **page** (`LoginPage`...) | Sabe hablar con una pantalla concreta |
| Los **utensilios** (cuchillo, tenedor) | Los **componentes** (`ChatDialogo`, `AgGrid`...) | Piezas que se usan en muchas pantallas |
| La **receta** de varios pasos | Los **flujos** (`login_como`...) | Una secuencia que se repite en muchos tests |
| El **libro de la despensa** | `core/vocabulario.py` y `datos/` | Los nombres y datos que se repiten |
| La **llave de la caja fuerte** | `.env` + `core/config.py` | Usuarios y contraseñas, fuera del código |

Si el cliente (el test) tuviera que saber dónde está cada cuchillo, cualquier cambio en la cocina rompería todos los pedidos.
Por eso **el test nunca busca botones: se lo pide a la page**.

---

## 2. El mapa de carpetas

```
testingEcommerce/
├── .env                  <- tus usuarios y contraseñas (NO se sube a git)
├── .env.example          <- plantilla para quien clone el repo
├── conftest.py           <- da a cada test la fixture `app`
├── run.py                <- el menú para ejecutar tests
│
├── core/                 <- los cimientos
│   ├── config.py         <- URL de la tienda + usuarios por rol
│   ├── base_page.py      <- cosas de Playwright que todas las pages usan
│   └── vocabulario.py    <- textos/selectores que aparecen en MÁS de una pantalla
│
├── pages/
│   ├── aplicacion.py     <- `app`: reparte todas las pages
│   └── shared/           <- una page por pantalla
│       ├── login_page.py, navegacion_page.py, catalogo_page.py ...
│       └── cuenta/       <- Mi cuenta, dividida en secciones
│           ├── datos.py, pedidos.py, direcciones.py, devoluciones.py
│
├── components/           <- piezas reutilizables (se usan en varias pantallas)
│   ├── ag_grid.py        <- la tabla AG Grid
│   ├── chat.py           <- el chat con la tienda
│   └── lista_tarjetas.py <- las listas de pedidos/direcciones/mensajes
│
├── flows/                <- recetas de varios pasos
│   ├── auth.py           <- login_como, abrir_mi_cuenta, abrir_administracion
│   ├── compra.py         <- de la home a "Finalizar compra"
│   └── cuenta.py         <- abrir pedidos / direcciones
│
├── datos/prueba.py       <- direcciones, tarjetas y producto de prueba
│
└── tests/
    ├── admin/ customer/ superadmin/   <- tests de la tienda, por rol
    └── framework/                     <- tests del propio framework (no necesitan la tienda)
```

**Regla para saber dónde mirar:** ¿se trata de _una_ pantalla? → `pages/`. ¿De algo que sale en _varias_? → `components/`
o `core/vocabulario.py`. ¿De varios pasos seguidos? → `flows/`. ¿Un dato de prueba? → `datos/`.

---

## 3. Antes y después: un test de verdad

**Antes** (8 líneas solo para entrar, copiadas 12 veces en 7 archivos):

```python
app_login.navegar()
app_navegacion.buscar_por_rol("link", name=app_navegacion._login_boton).click()
expect(app_login.buscar_por_texto(app_login._texto)).to_be_visible()
app_login.fill_box(app_login._email, app_login._correo_usuario)
app_login.fill_box(app_login._password, app_login._contrasenia_usuario)
app_login.buscar_por_rol("button", name=app_login._boton_entrar).nth(1).click()
toast = app_login.buscar_por_texto(app_login._login_exito)
expect(toast).to_be_visible()
```

**Ahora** (una línea):

```python
from flows.auth import login_como

def test_algo(self, app: Aplicacion):
    login_como(app, "customer")
```

Si mañana el botón "Entrar" cambia, se arregla **en** `LoginPage.enviar_credenciales` y todos los tests que entran quedan arreglados.

---

## 4. Cada pieza, explicada con un ejemplo

### 4.1 `config.py` — "¿quién soy y dónde estoy?"

Los usuarios ya no están escritos en el código. Se piden **por rol**:

```python
from core import config

usuario = config.usuario("customer")     # roles: "customer", "admin", "superadmin"
usuario.email                            # sale del .env: CUSTOMER_EMAIL
usuario.contrasenia                      # sale del .env: CUSTOMER_PASSWORD
config.BASE_URL                          # sale del .env: BASE_URL (por defecto http://localhost:5173/)
```

> Si falta una variable, el framework te lo dice claro: *"Falta la variable 'ADMIN_PASSWORD'. Copia .env.example a .env"*.

### 4.2 `vocabulario.py` — "un nombre, un sitio"

Aquí viven **solo** los textos y selectores que salen en **más de una pantalla**. Antes había
`finalizar_compra._cancelar` y `mi_cuenta._boton_cancelar`, los dos valían `"Cancelar"`. Ahora:

```python
# core/vocabulario.py
class Boton:
    CANCELAR = "Cancelar"

# en cualquier page:
from core.vocabulario import Boton
self.click_boton(Boton.CANCELAR)
```

Si la tienda cambia "Cancelar" por "Cerrar", **tocas una línea**.

### 4.3 `BasePage` — "las herramientas que todos tienen"

Todas las pages heredan de ella. Tiene lo básico: `navegar()`, `click_boton()`, `fill_box()`, `buscar_por_texto()`...
y un método muy usado que antes se escribía a mano en decenas de sitios:

```python
# antes
expect(app_login.buscar_por_texto("Dirección guardada")).to_be_visible()
# ahora
app.finalizar_compra.debe_ver("Dirección guardada")
# si el texto sale varias veces en pantalla:
app.finalizar_compra.debe_ver("Dirección guardada", primero=True)
```

### 4.4 Una page — "el camarero de una pantalla"

Tiene **dos cosas**: los locators (los "nombres" de lo que hay en pantalla) y **métodos** (lo que se puede hacer).
Los tests usan los métodos; los locators son privados (empiezan por `_`).

```python
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._email = Campo.EMAIL                  # <- viene del vocabulario
        self._boton_entrar = "Entrar"

    def enviar_credenciales(self, email, contrasenia):
        self.fill_box(self._email, email)
        self.fill_box(self._password, contrasenia)
        self.buscar_por_rol("button", name=self._boton_entrar).nth(1).click()

    def iniciar_sesion(self, usuario):             # login correcto: además comprueba el toast
        self.enviar_credenciales(usuario.email, usuario.contrasenia)
        self.debe_ver(self._login_exito)
```

Fíjate en que **hay dos métodos parecidos a propósito**: `enviar_credenciales` no comprueba nada (sirve también para el login
que debe _fallar_) e `iniciar_sesion` lo usa y añade la comprobación. **Se reutiliza, no se copia.**

### 4.5 Un componente — "un utensilio que sirve en varias cocinas"

Un componente es una page **de una pieza**, no de una pantalla entera. El chat sale en "Mis pedidos" **y** en la zona de
admin, así que no pertenece a ninguna de las dos:

```python
chat = app.mi_cuenta.chat
chat.abrir()
chat.enviar("Hola")
chat.debe_mostrar("Hola")
```

Y como cada ventana tiene su propia `Aplicacion`, el **mismo** componente sirve para el cliente y para el admin:

```python
admin = app.nueva_sesion()                 # otra ventana en incógnito
admin.mi_cuenta.chat.abrir_conversacion_con("Ana")
```

Otro ejemplo: la tabla del admin. Pulsar "Acciones > Aprobar" de una fila se repetía 3 veces; ahora es un método:

```python
AgGrid(page).accion_en_fila("P-2026-4274 Ana Redondo", "Aprobar")
```

### 4.6 Las secciones de "Mi cuenta" — "una clase enorme, partida en trozos"

`MiCuentaPage` tenía 104 líneas con 6 pantallas mezcladas. Ahora es un contenedor sin locators propios:

```python
app.mi_cuenta.datos          # Mis datos
app.mi_cuenta.pedidos        # Mis pedidos
app.mi_cuenta.direcciones    # Direcciones
app.mi_cuenta.devoluciones   # Devoluciones
app.mi_cuenta.chat           # Chat
```

Cada sección tiene **solo** lo suyo. Cuando buscas "el botón de cancelar pedido", sabes que está en `cuenta/pedidos.py`.

### 4.7 `Aplicacion` y la fixture `app` — "un solo mando para todo"

Antes había 7 fixtures (`app_login`, `app_navegacion`...) y cada test tenía que importarlas y pedirlas una a una.
Ahora **todo cuelga de** `app`:

```python
def test_algo(self, app: Aplicacion):
    app.login          # LoginPage
    app.navegacion     # NavegacionPage
    app.catalogo       # CatalogoPage
    app.mi_cuenta      # MiCuentaPage (y sus secciones)
```

Cada page se crea **solo la primera vez que la usas**, así que no gasta nada en las que no necesitas.

### 4.8 Los flujos — "recetas"

Un flujo es una función que encadena pasos que se repiten en muchos tests:

```python
# flows/auth.py (ya existe)
def login_como(app, rol):
    app.login.navegar()
    app.navegacion.ir_a_login()
    app.login.debe_mostrar_formulario()
    app.login.iniciar_sesion(config.usuario(rol))
```

Los flujos se **componen** entre ellos: `abrir_mi_cuenta` usa `login_como`, y `abrir_primer_pedido` usa `abrir_mi_cuenta`.
Un test de devoluciones empieza con **una línea** (`abrir_primer_pedido(app)`) en vez de 25.

### 4.9 `datos/prueba.py` — "los datos, aparte"

Antes "Ana Maria", "Calle Falsa 123", `4242424242424242`... estaban escritos dentro de cada test. Ahora:

```python
from datos.prueba import DIRECCION, TARJETA_VALIDA

app.finalizar_compra.rellenar_direccion(DIRECCION)
app.pago_tarjeta.pagar_con_tarjeta(TARJETA_VALIDA)
```

---

## 5. Recetas: "quiero hacer X, ¿qué toco?"

### 5.1 Un botón nuevo en una pantalla que ya existe

Ejemplo inventado: en Mis pedidos aparece un botón "Repetir pedido".

1. **¿Ese texto ya existe en otra pantalla?** Búscalo en `core/vocabulario.py`. Si está → úsalo. Si no, sigue.
2. Añade el locator **en la page de esa pantalla** (`cuenta/pedidos.py`):
   ```python
    self._boton_repetir_pedido: str = "Repetir pedido"
   ```
3. Añade un **método** que diga qué se hace con él:
   ```python
    def repetir_pedido(self) -> None:
        self.click_boton(self._boton_repetir_pedido)
        self.debe_ver("Pedido añadido al carrito")
   ```
4. En el test: `app.mi_cuenta.pedidos.repetir_pedido()`. Fin. El test **no** conoce el texto del botón.

### 5.2 Un texto que **ya existe** y quieres usar en otra pantalla

Es justo el caso que querías evitar ("el botón se llama igual en otro sitio"). **No** crees `_boton_cancelar_2`:

1. Muévelo a `core/vocabulario.py` (si no estaba ya) y dale un nombre claro: `Boton.CANCELAR`.
2. En las dos pages: `self._cancelar = Boton.CANCELAR`.

Regla: **si lo escribes por segunda vez, es hora de moverlo al vocabulario.**

### 5.3 Una pantalla nueva (ejemplo inventado: "Suscripción")

1. Crea `pages/shared/suscripcion_page.py`:
   ```python
    class SuscripcionPage(BasePage):
        def __init__(self, page):
            super().__init__(page)
            self._titulo = "Tu suscripción"
            self._boton_darse_de_baja = "Darme de baja"

        def darse_de_baja(self):
            self.click_boton(self._boton_darse_de_baja)
            self.debe_ver("Suscripción cancelada")
   ```
2. Regístrala en `pages/aplicacion.py` (3 líneas):
   ```python
    @cached_property
    def suscripcion(self) -> SuscripcionPage:
        return SuscripcionPage(self.page)
   ```
3. Úsala: `app.suscripcion.darse_de_baja()`. **No** hay que tocar `conftest.py` ni importar nada en el test.

Si la pantalla es una **sección de Mi cuenta**, créala en `pages/shared/cuenta/` y cuélgala de `MiCuentaPage` (un `self.suscripcion = SuscripcionSeccion(page)` en su `__init__`).

### 5.4 Un componente nuevo (ejemplo inventado: un "Selector de fechas")

¿Aparece en **dos o más** pantallas? Entonces es un componente:

```python
# components/selector_fecha.py
class SelectorFecha(BasePage):
    def elegir(self, dia: int, mes: str):
        self.click_boton("Abrir calendario")
        self.click_boton(mes)
        self.click_boton(str(dia))
```

Y se **cuelga** de las pages que lo usan: `self.fecha = SelectorFecha(page)` → `app.pedidos.fecha.elegir(14, "Marzo")`.

### 5.5 Un flujo nuevo

¿Vas a escribir los mismos 4+ pasos en un segundo test? Hazlo flujo en `flows/`:

```python
def reembolsar_primera_devolucion(admin, fila):
    abrir_administracion(admin)
    admin.mi_cuenta.devoluciones.abrir()
    admin.mi_cuenta.devoluciones.reembolsar(fila)
```

### 5.6 Un test nuevo

```python
# tests/customer/test_suscripcion.py
from flows.auth import abrir_mi_cuenta
from pages.aplicacion import Aplicacion

class TestSuscripcion:
    def test_darse_de_baja(self, app: Aplicacion):
        abrir_mi_cuenta(app)
        app.suscripcion.darse_de_baja()
```

Crea el archivo y `run.py` **lo detecta solo**, sin reiniciar el menú. Fíjate: **no hay** `import` **de fixtures ni de pages**; solo `app`.

### 5.7 "La tienda cambió un texto"

Busca el texto antiguo con la búsqueda del editor (`"Guardar dirección"`). Debería salir **una vez** en `pages/` o `vocabulario.py`.
Cámbialo ahí. Si sale en más de un sitio, ya sabes qué mover al vocabulario (receta 5.2).

---

## 6. ¿Dónde va esto? (chuleta)

| Tengo... | Va en... |
|---|---|
| Un texto/selector de **una** pantalla | atributo `_algo` de su page |
| Un texto/selector que sale en **2+** pantallas | `core/vocabulario.py` |
| Algo que se **hace** (clic + comprobar) | método de la page |
| Una pieza que sale en 2+ pantallas (chat, tabla, lista) | `components/` |
| 4+ pasos que se repiten en varios tests | `flows/` |
| Un nombre, dirección, tarjeta de prueba | `datos/prueba.py` |
| Un correo o contraseña | `.env` (nunca en el código) |
| Un `expect(...)` | casi siempre `debe_ver(...)` o un método de la page |

---

## 7. Lo que NO hay que hacer

- Escribir un texto de la tienda **dentro de un test** (salvo comprobaciones de una sola vez, muy específicas).
- Crear `_boton_x` y `_boton_x2` con el mismo valor.
- Que un test llame a `app.login._email` y rellene campos a mano si ya existe un método (`enviar_credenciales`).
- Pedir los datos de un usuario a una page (`app.login._correo_usuario` ya no existe): usa `config.usuario("customer")`.
- Copiar los pasos de login: usa `login_como(app, rol)`.
- Importar fixtures desde `conftest` en los tests (pytest las encuentra solo).

---

## 8. Puesta en marcha

```bash
pip install -r requirements.txt
playwright install
copy .env.example .env     # y rellena los usuarios reales
python run.py              # menú interactivo
python run.py tests/framework --headless    # tests del framework (no necesitan la tienda)
```

---

## 9. Lo que se queda para más adelante

- **Locators con tipo** (`Boton("Entrar")`, `Campo("email")`): no se hizo; los locators siguen siendo texto. Es el siguiente paso si quieres
que un test no tenga que saber si algo es CSS o texto.
- **Login una sola vez por rol** con `storage_state` de Playwright (hoy cada test entra de cero; es lo que más acelera la suite).
- `data-testid` **en la tienda**: con ellos los tests no dependerían de los textos y no se romperían al cambiar un copy.
- Dos cosas del código original que **se respetaron tal cual** pero conviene revisar (hay un comentario `OJO`/`TODO` en el código):
el chat del admin escribe en la ventana del cliente (`tests/customer/test_chat.py`), y al cancelar un pedido nunca se comprueba el mensaje de "cancelado".

## 10. Titulo de prueba para mostrar a ana

**esto estará en negrita** lo demas estará en normal *y esto será una prueba*

```
    print("hola mundo")
```

1. enumeracion
2. test

- test
- test2