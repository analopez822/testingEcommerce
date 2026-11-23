from flows.auth import abrir_mi_cuenta
from pages.aplicacion import Aplicacion


class TestMiCuentaPage:
    """Suite de pruebas para la pagina Mi cuenta"""

    def test_mi_cuenta(self, app: Aplicacion):
        abrir_mi_cuenta(app)
        # comprobando titulo y secciones de Mis Datos
        app.mi_cuenta.datos.debe_mostrar_secciones()
        # comprobando elementos de panel izquierdo
        app.mi_cuenta.recorrer_panel()
        app.page.wait_for_timeout(2000)

    def test_mis_datos(self, app: Aplicacion):
        datos = app.mi_cuenta.datos
        app.login.debugger()
        abrir_mi_cuenta(app)
        datos.debe_mostrar_titulo()
        # actualizando telefono en Datos Personales
        datos.actualizar_telefono("123456789")

        # # actualizando correo en Correo Electronico
        # Comento esta seccion porque requiere un cambio manual de correo electronico cada vez que se ejecuta
        # datos.fill_box(datos._nuevo_email, config.usuario("admin").email)
        # datos.fill_box(datos._nueva_contrasenia, config.usuario("customer").contrasenia)
        # datos.click_boton(datos._boton_correo)
        # datos.debe_ver(datos._email_con_codigo_enviado)
        # codigo = input("Tienes un cambio pendiente de correo. Escribe el código que te hemos enviado.")
        # datos.fill_box(datos._codigo_verificacion_correo, codigo)
        # datos.click_boton(datos._boton_confirmar)
        # app.page.wait_for_timeout(2000)
        # datos.debe_ver(datos._email_actualizado)

        # Descargando json file desde Descargar mis Datos
        ruta_datos = datos.descargar_mis_datos()
        assert ruta_datos.exists(), f"El archivo json no existe en el directorio: {ruta_datos}"
        print(f"Datos descargados en: {ruta_datos}")
        datos.abrir_archivo(ruta_datos)

        # Eliminando cuenta desde Eliminar Cuenta
        datos.abrir_dialogo_baja("Me doy de baja")
        datos.cerrar_dialogo_baja()
        datos.pedir_codigo_baja()
        codigo_baja = input("Escribe el código de verificacion de cambio de cuenta que te hemos enviado.")
        datos.confirmar_baja(codigo_baja)
        datos.cancelar_baja()
        app.page.wait_for_timeout(2000)
