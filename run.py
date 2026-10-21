import os
import sys
import ast
import argparse
import pytest
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


RAIZ = Path(__file__).resolve().parent
DIRECTORIO_TESTS = RAIZ / "tests"
DIRECTORIO_REPORTES = RAIZ / "reports"
REPORTE_HTML = DIRECTORIO_REPORTES / "ejecucion_report.html"

# Mismo criterio que pytest.ini (python_files = test_*.py)
PREFIJO_ARCHIVO = "test_"

# page.pause()


@dataclass
class ArchivoPrueba:
    ruta: Path
    pruebas: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class CarpetaPruebas:
    ruta: Path
    subcarpetas: List["CarpetaPruebas"] = field(default_factory=list)
    archivos: List[ArchivoPrueba] = field(default_factory=list)

    def total_archivos(self) -> int:
        return len(self.archivos) + sum(c.total_archivos() for c in self.subcarpetas)

    def total_pruebas(self) -> int:
        return sum(len(a.pruebas) for a in self.archivos) + sum(c.total_pruebas() for c in self.subcarpetas)


def ruta_relativa(ruta: Path) -> str:
    """Ruta relativa a la raíz del proyecto con '/' (formato que espera pytest, también en Windows)."""
    return ruta.relative_to(RAIZ).as_posix()


def extraer_pruebas(ruta: Path) -> ArchivoPrueba:
    """
    Analiza un archivo con AST (sin importarlo) y extrae sus pruebas:
    funciones `test_*` sueltas y métodos `test_*` de clases `Test*`.
    """
    archivo = ArchivoPrueba(ruta=ruta)

    try:
        arbol = ast.parse(ruta.read_text(encoding="utf-8"), filename=str(ruta))
    except SyntaxError as exc:
        archivo.error = f"error de sintaxis en la línea {exc.lineno}"
        return archivo

    # Solo nodos de la raíz del documento: evita duplicar métodos de clase
    for nodo in arbol.body:
        if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)) and nodo.name.startswith("test_"):
            archivo.pruebas.append(nodo.name)

        elif isinstance(nodo, ast.ClassDef) and nodo.name.startswith("Test"):
            for nodo_clase in nodo.body:
                if isinstance(nodo_clase, (ast.FunctionDef, ast.AsyncFunctionDef)) and nodo_clase.name.startswith("test_"):
                    archivo.pruebas.append(f"{nodo.name}::{nodo_clase.name}")

    return archivo


def descubrir_pruebas(ruta: Path = DIRECTORIO_TESTS) -> Optional[CarpetaPruebas]:
    """
    Recorre `tests/` de forma recursiva (a cualquier profundidad) y devuelve el árbol
    de carpetas y archivos de prueba. Las carpetas sin ningún archivo de prueba se omiten.
    """
    if not ruta.is_dir():
        return None

    carpeta = CarpetaPruebas(ruta=ruta)

    for entrada in sorted(ruta.iterdir(), key=lambda e: e.name.lower()):
        if entrada.is_dir():
            if entrada.name.startswith((".", "_")):   # __pycache__, .pytest_cache, etc.
                continue
            subcarpeta = descubrir_pruebas(entrada)
            if subcarpeta is not None:
                carpeta.subcarpetas.append(subcarpeta)
        elif entrada.name.startswith(PREFIJO_ARCHIVO) and entrada.suffix == ".py":
            carpeta.archivos.append(extraer_pruebas(entrada))

    if not carpeta.subcarpetas and not carpeta.archivos:
        return None
    return carpeta


def pedir_opcion(mensaje: str) -> str:
    try:
        return input(mensaje).strip().upper()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def menu_carpeta(carpeta: CarpetaPruebas, es_raiz: bool = False) -> Optional[str]:
    """
    Menú de una carpeta: ejecutar todo su contenido, entrar a una subcarpeta o elegir un archivo.
    Devuelve el objetivo de pytest, o None si el usuario vuelve atrás.
    """
    entradas = carpeta.subcarpetas + carpeta.archivos
    ruta_visible = ruta_relativa(carpeta.ruta)

    while True:
        print("\n==================================================")
        print(" FRAMEWORK DE EJECUCIÓN DINÁMICA DE PRUEBAS")
        print(f" Ubicación: {ruta_visible}")
        print("==================================================")
        print("0. Ejecutar toda la suite (Regresión Completa)" if es_raiz
              else f"0. Ejecutar todo {ruta_visible}")

        for idx, entrada in enumerate(entradas, 1):
            if isinstance(entrada, CarpetaPruebas):
                print(f"{idx}. [Carpeta] {entrada.ruta.name}/  "
                      f"({entrada.total_archivos()} archivos, {entrada.total_pruebas()} pruebas)")
            else:
                detalle = f"({entrada.error})" if entrada.error else f"({len(entrada.pruebas)} pruebas)"
                print(f"{idx}. Archivo: {entrada.ruta.name}  {detalle}")

        print("S. Salir del framework" if es_raiz else "V. Volver")
        print("==================================================")

        seleccion = pedir_opcion("Seleccione una opción: ")

        if es_raiz and seleccion == "S":
            sys.exit(0)
        if not es_raiz and seleccion == "V":
            return None
        if seleccion == "0":
            return ruta_relativa(carpeta.ruta)

        if seleccion.isdigit() and 1 <= int(seleccion) <= len(entradas):
            entrada = entradas[int(seleccion) - 1]
            if isinstance(entrada, CarpetaPruebas):
                objetivo = menu_carpeta(entrada)
            else:
                objetivo = seleccionar_funcion(entrada)
            if objetivo is not None:
                return objetivo
            continue

        print("[ERROR] Opción no válida.")


def seleccionar_funcion(archivo: ArchivoPrueba) -> Optional[str]:
    """Permite aislar la ejecución a un nivel atómico (una sola prueba)."""
    ruta_archivo = ruta_relativa(archivo.ruta)

    while True:
        print(f"\n--- Pruebas disponibles en {ruta_archivo} ---")
        print("0. Ejecutar todo el archivo")

        for idx, funcion in enumerate(archivo.pruebas, 1):
            print(f"{idx}. {funcion}")

        print("V. Volver")

        seleccion = pedir_opcion("Seleccione la prueba a ejecutar: ")

        if seleccion == "V":
            return None
        if seleccion == "0":
            return ruta_archivo
        if seleccion.isdigit() and 1 <= int(seleccion) <= len(archivo.pruebas):
            # Ejecución atómica: ruta/archivo.py::TestClase::test_metodo
            return f"{ruta_archivo}::{archivo.pruebas[int(seleccion) - 1]}"

        print("[ERROR] Opción no válida.")


def construir_argumentos(objetivos: List[str], args: argparse.Namespace) -> List[str]:
    argumentos_pytest = [
        *objetivos,
        "-v", "-s",
        f"--html={REPORTE_HTML.relative_to(RAIZ).as_posix()}", "--self-contained-html",
        "--screenshot=only-on-failure",
    ]
    if not args.headless:
        argumentos_pytest += ["--headed", f"--slowmo={args.slowmo}"]
    if args.browser:
        argumentos_pytest.append(f"--browser={args.browser}")
    return argumentos_pytest


def ejecutar_pytest(objetivos: List[str], args: argparse.Namespace, debug: bool) -> int:
    # El modo debug se fija siempre, para que no se arrastre entre ejecuciones del menú
    os.environ["DEBUG_PAUSA"] = "1" if debug else "0"
    if debug and args.headless:
        print("[AVISO] El modo debug (page.pause) necesita navegador visible; no use --headless.")

    DIRECTORIO_REPORTES.mkdir(exist_ok=True)
    argumentos_pytest = construir_argumentos(objetivos, args)

    print(f"\n[INFO] Ejecutando: pytest {' '.join(argumentos_pytest)}\n")
    return int(pytest.main(argumentos_pytest))


def validar_objetivos(objetivos: List[str]) -> List[str]:
    """Para uso no interactivo: acepta rutas (carpeta, archivo o nodeid) y comprueba que existan."""
    validos = []
    for objetivo in objetivos:
        ruta_texto, separador, nodo = objetivo.partition("::")
        ruta = (RAIZ / ruta_texto).resolve()
        if not ruta.exists() or DIRECTORIO_TESTS not in (ruta, *ruta.parents):
            print(f"[ERROR] '{objetivo}' no existe dentro de '{DIRECTORIO_TESTS.name}/'.")
            sys.exit(2)
        validos.append(f"{ruta_relativa(ruta)}{separador}{nodo}")
    return validos


def ejecutar_motor(args: argparse.Namespace) -> None:
    """Punto de entrada principal del orquestador."""

    while True:
        raiz = descubrir_pruebas()   # se redescubre en cada vuelta: las pruebas nuevas aparecen sin reiniciar

        if raiz is None:
            print(f"[AVISO] No hay pruebas disponibles en '{DIRECTORIO_TESTS}'.")
            return

        objetivo = menu_carpeta(raiz, es_raiz=True)

        respuesta_debug = pedir_opcion("¿Activar modo debug? (s/n): ")
        debug = respuesta_debug == "S"
        if debug:
            print("debug activado")

        ejecutar_pytest([objetivo], args, debug)

        pedir_opcion("\nPresione ENTER para continuar...")


def leer_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecutor de pruebas E2E (menú interactivo o línea de comandos).")
    parser.add_argument("objetivos", nargs="*",
                        help="Carpetas, archivos o nodeids a ejecutar sin menú (ej: tests/admin). Sin valor: menú interactivo.")
    parser.add_argument("--headless", action="store_true", help="Ejecutar sin abrir el navegador (CI).")
    parser.add_argument("--slowmo", type=int, default=700, help="Ralentización en ms entre acciones (solo con navegador visible).")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], help="Navegador (por defecto el de pytest-playwright).")
    parser.add_argument("--debug", action="store_true", help="Activar DEBUG_PAUSA (page.pause) en modo no interactivo.")
    return parser.parse_args()


if __name__ == "__main__":
    os.chdir(RAIZ)   # rutas relativas (reports/, test-results/) iguales sin importar desde dónde se lance
    opciones = leer_argumentos()

    if opciones.objetivos:
        sys.exit(ejecutar_pytest(validar_objetivos(opciones.objetivos), opciones, opciones.debug))

    ejecutar_motor(opciones)
