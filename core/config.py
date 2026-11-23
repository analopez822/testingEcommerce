"""
Configuracion central del framework: URL de la tienda y usuarios de prueba por rol.

Los valores salen de variables de entorno o del archivo `.env` (que NO se sube a git).
Plantilla: `.env.example`. Un test nunca escribe un correo o una contrasenia a mano:
pide el usuario por su rol -> `usuario("customer")`.
"""
import os
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _cargar_env(ruta: Path = RAIZ / ".env") -> None:
    """Lee lineas CLAVE=VALOR del .env sin pisar variables que ya existan en el entorno."""
    if not ruta.exists():
        return
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        os.environ.setdefault(clave.strip(), valor.strip().strip("\"'"))


_cargar_env()


def _requerida(nombre: str) -> str:
    valor = os.environ.get(nombre)
    if not valor:
        raise RuntimeError(
            f"Falta la variable '{nombre}'. Copia .env.example a .env y rellénala (ver core/config.py)."
        )
    return valor


@dataclass(frozen=True)
class Usuario:
    rol: str
    email: str
    contrasenia: str


ROLES = ("customer", "admin", "superadmin")

BASE_URL: str = os.environ.get("BASE_URL", "http://localhost:5173/")
CONTRASENIA_INCORRECTA: str = "Incorrecta"


def usuario(rol: str) -> Usuario:
    """Devuelve el usuario de prueba de un rol ('customer', 'admin' o 'superadmin')."""
    if rol not in ROLES:
        raise ValueError(f"Rol desconocido '{rol}'. Roles validos: {', '.join(ROLES)}")
    prefijo = rol.upper()
    return Usuario(rol=rol, email=_requerida(f"{prefijo}_EMAIL"), contrasenia=_requerida(f"{prefijo}_PASSWORD"))
