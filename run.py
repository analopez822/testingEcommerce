import os
import sys
import ast
import pytest
from typing import List, Tuple, Dict


DIRECTORIO_TESTS = "tests"

# page.pause()

def descubrir_pruebas() -> Dict[str, List[str]]:
    """
    Analiza el directorio de pruebas y extrae los nombres de los archivos
    y las funciones de prueba evitando duplicados de clases.
    """
    estructura_pruebas = {}

    if not os.path.exists(DIRECTORIO_TESTS):
        print(f"[ERROR] No se encontró el directorio '{DIRECTORIO_TESTS}'.")
        return estructura_pruebas

    archivos = [f for f in os.listdir(DIRECTORIO_TESTS) if f.startswith("test_") and f.endswith(".py")]

    for archivo in archivos:
        ruta_completa = os.path.join(DIRECTORIO_TESTS, archivo)
        estructura_pruebas[archivo] = []

        with open(ruta_completa, "r", encoding="utf-8") as file:
            nodo_arbol = ast.parse(file.read(), filename=archivo)

            # SOLUCIÓN: Iterar solo por los nodos de la raíz del documento
            for nodo in nodo_arbol.body:

                # 1. Si encuentra una función suelta en la raíz del archivo
                if isinstance(nodo, ast.FunctionDef) and nodo.name.startswith("test_"):
                    estructura_pruebas[archivo].append(nodo.name)

                # 2. Si encuentra una clase de prueba
                elif isinstance(nodo, ast.ClassDef) and nodo.name.startswith("Test"):
                    # Itera SOLO dentro del cuerpo de esta clase específica
                    for nodo_clase in nodo.body:
                        if isinstance(nodo_clase, ast.FunctionDef) and nodo_clase.name.startswith("test_"):
                            estructura_pruebas[archivo].append(f"{nodo.name}::{nodo_clase.name}")

    return estructura_pruebas


def mostrar_menu_principal(pruebas: Dict[str, List[str]]) -> Tuple[str, str]:
    """Muestra la interfaz de línea de comandos y captura la selección del usuario."""

    archivos = list(pruebas.keys())

    while True:
        print("\n==================================================")
        print(" FRAMEWORK DE EJECUCIÓN DINÁMICA DE PRUEBAS")
        print("==================================================")
        print("0. Ejecutar toda la suite (Regresión Completa)")

        for idx, archivo in enumerate(archivos, 1):
            print(f"{idx}. Archivo: {archivo}")

        print("S. Salir del framework")
        print("==================================================")

        seleccion = input("Seleccione una opción: ").strip().upper()

        if seleccion == 'S':
            sys.exit(0)
        if seleccion == '0':
            return "all", ""

        try:
            indice = int(seleccion) - 1
            if 0 <= indice < len(archivos):
                archivo_seleccionado = archivos[indice]
                return archivo_seleccionado, seleccionar_funcion(archivo_seleccionado, pruebas[archivo_seleccionado])
        except ValueError:
            pass

        print("[ERROR] Opción no válida.")


def seleccionar_funcion(archivo: str, funciones: List[str]) -> str:
    """Permite aislar la ejecución a un nivel atómico (una sola prueba)."""

    while True:
        print(f"\n--- Pruebas disponibles en {archivo} ---")
        print("0. Ejecutar todo el archivo")

        for idx, funcion in enumerate(funciones, 1):
            print(f"{idx}. {funcion}")

        print("V. Volver al menú principal")

        seleccion = input("Seleccione la prueba a ejecutar: ").strip().upper()

        if seleccion == 'V':
            return "back"
        if seleccion == '0':
            return "all"

        try:
            indice = int(seleccion) - 1
            if 0 <= indice < len(funciones):
                return funciones[indice]
        except ValueError:
            pass

        print("[ERROR] Opción no válida.")


def ejecutar_motor() -> None:
    """Punto de entrada principal del orquestador."""

    pruebas_disponibles = descubrir_pruebas()

    if not pruebas_disponibles:
        print("[AVISO] No hay pruebas disponibles para ejecutar.")
        return

    while True:
        archivo, funcion = mostrar_menu_principal(pruebas_disponibles)

        if funcion == "back":
            continue

        respuesta_debug = input("¿Activar modo debug? (s/n): ").strip().lower()
        if respuesta_debug == "s":
            os.environ["DEBUG_PAUSA"] = "1"
            print("debug activado")

        # Construcción dinámica de los parámetros para Pytest
        argumentos_pytest = ["--headed", "-v", "-s", "--slowmo=700", "--html=reports/ejecucion_report.html", "--self-contained-html", "--screenshot=only-on-failure"]  #, "--browser=firefox"

        if archivo == "all":
            argumentos_pytest.insert(0, DIRECTORIO_TESTS)
        elif funcion == "all":
            argumentos_pytest.insert(0, f"{DIRECTORIO_TESTS}/{archivo}")
        else:
            # Ejecución atómica: ruta/archivo.py::TestClase::test_metodo
            argumentos_pytest.insert(0, f"{DIRECTORIO_TESTS}/{archivo}::{funcion}")

        print(f"\n[INFO] Ejecutando: pytest {' '.join(argumentos_pytest)}\n")
        pytest.main(argumentos_pytest)

        input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    ejecutar_motor()