"""Flujo de compra: de la home hasta la pantalla 'Finalizar compra' con la direccion rellena."""
from core import config
from datos import prueba
from pages.aplicacion import Aplicacion


def llegar_a_finalizar_compra(app: Aplicacion, aniadir_unidad: bool = True, texto_ficha: str = "Disponible") -> None:
    """
    Catalogo > buscar producto > añadir al carrito > carrito > Finalizar compra > login > direccion guardada.
    `texto_ficha` es un texto que debe verse en la ficha del producto para dar por buena la pagina.
    """
    app.login.navegar()
    app.navegacion.ir_al_catalogo()
    app.catalogo.debe_ver(app.catalogo._texto_catalogo)
    app.catalogo.abrir_producto(prueba.PRODUCTO)
    app.catalogo.debe_ver(texto_ficha)
    if aniadir_unidad:
        app.catalogo.aniadir_unidad()
    app.catalogo.aniadir_al_carrito(prueba.NOMBRE_PRODUCTO)
    app.navegacion.abrir_carrito()
    app.catalogo.debe_ver(app.catalogo._aviso_carrito_invitado)
    app.catalogo.ir_a_finalizar_compra()
    # sin sesion, la tienda manda al login y despues vuelve a 'Finalizar compra'
    app.login.debe_mostrar_formulario()
    app.login.iniciar_sesion(config.usuario("customer"))
    app.finalizar_compra.debe_mostrar_pagina()
    app.finalizar_compra.cargar_direccion(prueba.DIRECCION)
