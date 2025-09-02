import flet as ft
import inicio
import login
import crearADMIN
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.cambiar_contraseña import cambiar_contraseña_admin

def main(page: ft.Page):
    # ---------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    CARD_BACKGROUND = "#FFFFFF"
    page.bgcolor = "white"
    page.padding = 0
    page.spacing = 0
    page.window_width = 1920
    page.window_height = 1080

    #------------- OBTENER TOKEN--------------------

    def obtener_token(page):
        return getattr(page, "session_token", None)

    # ---------------------- FUNCIONES AUXILIARES ----------------------
    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        if isinstance(e.control.title, ft.Text):
            title = e.control.title.value
            if title == "Crear Usuario Administrador":
                crearADMIN.main(page)
            if title == "Inicio":
                inicio.main(page)
            if title == "Configuración de cuenta":
                config_cuenta.main(page)
        page.drawer.open = False
        page.update()

    def open_drawer(e):
        page.drawer.open = True
        page.update()

    def mostrar_snackbar(mensaje, exito=True):
        """Muestra SnackBar con estilo uniforme"""
        sb = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.Colors.GREEN if exito else ft.Colors.RED,
            duration=3000
        )
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def cerrar_sesion(e):
        respuesta = cerrar_sesion_api()
        page.clean()
        login.main(page)

        if respuesta.get("success"):
            mostrar_snackbar("Sesión cerrada correctamente.", exito=True)
        else:
            mostrar_snackbar(respuesta.get("message", "Error al cerrar sesión"), exito=False)

        # ---------------------------------------------------------------

    # ---------------------- DRAWER ----------------------
    page.drawer = ft.NavigationDrawer(
        bgcolor="#FFFFFF",
        controls=[
            ft.Container(
                padding=ft.padding.all(10),
                content=ft.Column(
                    spacing=25,
                    controls=[
                        ft.Container(
                            alignment=ft.alignment.top_left,
                            padding=ft.padding.only(top=10, left=10),
                            content=ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color=ft.Colors.BLACK,
                                icon_size=28,
                                on_click=close_drawer,
                            ),
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.HOME_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Inicio", size=18, color=TEXT_COLOR, font_family="Oswald"),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Configuración de cuenta", size=18, color=TEXT_COLOR, font_family="Oswald"),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Crear Usuario Administrador", size=18, color=TEXT_COLOR, font_family="Oswald"),
                            on_click=on_drawer_item_click,
                        ),
                    ],
                ),
            )
        ],
    )

    # ---------------------- HEADER ----------------------
    header = ft.Container(
        bgcolor="#F8F8F8",
        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            spacing=20,
            controls=[
                ft.IconButton(icon=ft.Icons.MENU, icon_color="#000000", on_click=open_drawer),
                ft.Row(
                    spacing=1,
                    controls=[
                        ft.Image(src="../img/logo.jpg", width=82, height=82),
                        ft.Text("Cali", color=PRIMARY_COLOR, size=40, font_family="Oswald"),
                        ft.Text("Trabaja", color="#000000", size=40, font_family="Oswald"),
                    ],
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center_right,
                    content=ft.ElevatedButton(
                        "Cerrar Sesión",
                        bgcolor="#3EAEB1",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=30),
                            padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
                            text_style=ft.TextStyle(font_family="Oswald"),
                        ),
                        on_click=cerrar_sesion
                    ),
                ),
            ],
        ),
    )

    def cambiar_contraseña(page, actual_contrasena, nueva_contrasena, confirmar_contrasena):
        token = obtener_token(page)

        if not token:
            page.add(ft.Text("Debes iniciar sesion primero"))
            return []

        datos = {}
        if actual_contrasena:
            datos["actual_contrasena"] = actual_contrasena

        if nueva_contrasena:
            datos["nueva_contrasena"] = nueva_contrasena

        if confirmar_contrasena:
            datos["confirmar_contrasena"] = confirmar_contrasena

        print("Datos enviados: ", datos)

        respuesta= cambiar_contraseña_admin(token, datos)

        if respuesta.get("success")==True:
            print(respuesta["success"])
            inicio.main(page)

        return respuesta

    def guardar_contraseña(e):
        contraseña_actual = contraseña_actual_field.value.strip() if contraseña_actual_field.value else None
        nueva_contraseña = nueva_contraseña_field.value.strip() if nueva_contraseña_field.value else None
        repetir_contraseña = repetir_contraseña_field.value.strip() if repetir_contraseña_field.value else None

        print(
            f"CONTRASEÑA ACTUAL: {contraseña_actual}, NUEVA CONTRASEÑA: {nueva_contraseña}, REPETIR CONTRASEÑA: {repetir_contraseña}")

        respuesta = cambiar_contraseña(page, contraseña_actual, nueva_contraseña, repetir_contraseña)

        if respuesta.get("success"):
            mostrar_snackbar("Contraseña cambiada correctamente ", exito=True)
            page.clean()
            config_cuenta.main(page)  # volver a la configuración de cuenta
        else:
            mostrar_snackbar(respuesta.get("message", "Error al cambiar la contraseña"), exito=False)

    #Inicializar los parametros
    contraseña_actual_field = ft.TextField(password=True, can_reveal_password=True,border_radius=8, bgcolor="#E0E0E0", width=600)
    nueva_contraseña_field = ft.TextField(  password=True, can_reveal_password=True,border_radius=8, bgcolor="#E0E0E0", width=600)
    repetir_contraseña_field = ft.TextField( password=True, can_reveal_password=True,border_radius=8, bgcolor="#E0E0E0", width=600)


    # Contenido formulario
    contenido = ft.Row(

        alignment="center",  # Centra horizontalmente
        controls=[
            ft.Container(
                width=600,  # Ancho fijo del bloque
                margin=ft.margin.only(top=50),
                content=ft.Column(
                    spacing=12,
                    horizontal_alignment="start",  # Contenido alineado a la izquierda
                    controls=[
                        ft.Text("Cambiar contraseña", size=22, weight="bold", color="#3EAEB1", font_family="Oswald"),

                        ft.Text("Contraseña actual", size=18, color="black", font_family="Oswald"),
                        contraseña_actual_field,

                        ft.Text("Nueva contraseña", size=18, color="black", font_family="Oswald"),
                        nueva_contraseña_field,

                        ft.Text("Repetir contraseña", size=18, color="black", font_family="Oswald"),
                        repetir_contraseña_field,

                        ft.Row(
                            alignment="start",  # Botones alineados al inicio
                            spacing=20,
                            controls=[
                                ft.ElevatedButton(
                                    "Cancelar",
                                    bgcolor="#F5F5F5",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=30),
                                        side=ft.BorderSide(width=2, color="#D9D9D9"),
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                        text_style=ft.TextStyle(font_family="Oswald", size=18),
                                    ),
                                    on_click=lambda e: (page.clean(), config_cuenta.main(page))
                                ),
                                ft.ElevatedButton(
                                    "Guardar cambios",
                                    bgcolor="#F5F5F5",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        side=ft.BorderSide(width=2, color="#2FBDB3"),
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                        text_style=ft.TextStyle(font_family="Oswald", size=18),
                                    ),
                                    on_click=guardar_contraseña
                                ),
                            ]
                        ),
                    ]
                )
            )
        ]
    )




    # Layout principal
    page.add(
        ft.Column(
            expand=True,
            controls=[
                header,
                contenido,
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.all(40),
                )
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
