"""Datos de prueba reutilizables. Los tests piden aqui los datos en vez de escribirlos en cada test."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Direccion:
    nombre: str
    calle: str
    codigo_postal: str
    ciudad: str
    provincia: str
    telefono: str
    notas: str


@dataclass(frozen=True)
class Tarjeta:
    numero: str
    caducidad: str
    cvc: str
    pais: str
    email: str
    movil: str
    nombre: str


DIRECCION = Direccion(
    nombre="Ana Maria", calle="Calle Falsa 123", codigo_postal="12345", ciudad="Madrid",
    provincia="Madrid", telefono="123456789", notas="Notas de entrega",
)

# Campos que cambia el test de "editar direccion"
DIRECCION_EDITADA = Direccion(
    nombre=DIRECCION.nombre, calle=DIRECCION.calle, codigo_postal=DIRECCION.codigo_postal, ciudad=DIRECCION.ciudad,
    provincia="Barcelona", telefono="987654321", notas="Notas actualizadas",
)

TARJETA_VALIDA = Tarjeta(
    numero="4242424242424242", caducidad="12/26", cvc="123", pais="Albania",
    email="correo@yahoo.es", movil="07400123456", nombre="Ana Redondo",
)

PRODUCTO = "chocorramo"                 # texto de busqueda y slug de la URL: /catalogo/producto-chocorramo
NOMBRE_PRODUCTO = "Chocorramo Unidad"   # como se muestra en la tienda
