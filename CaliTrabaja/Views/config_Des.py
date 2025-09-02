import flet as ft
import inicio
import login
import crearADMIN
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.deshabilitar_admin import deshabilitar_admin

def main(page: ft.Page):
    def obtener_token(page):
        return getattr(page, "session_token", None)
    # ---------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    page.bgcolor = "white"
    page.padding = 0
    page.spacing = 0
    page.window_width = 1920
    page.window_height = 1080

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

    def deshabilitar_usuario(page, confirmar_contraseña):
        token = obtener_token(page)

        if not token:
            mostrar_snackbar("Debes iniciar sesión primero.", exito=False)
            return {"success": False, "message": "Token no encontrado."}

        datos = {}

        if confirmar_contraseña:
            datos["contrasena"] = confirmar_contraseña

        print("Contraseña enviada:", datos)

        respuesta = deshabilitar_admin(token, datos)

        if respuesta.get("success"):
            mostrar_snackbar("Cuenta deshabilitada correctamente.", exito=True)
            page.clean()
            login.main(page)
        else:
            mostrar_snackbar(respuesta.get("message", "Error al deshabilitar la cuenta"), exito=False)

        return respuesta

    def capturar_contraseña(e):
        confirmar_contraseña = confirmar_contraseña_field.value.strip() if confirmar_contraseña_field.value else None

        if not confirmar_contraseña:
            mostrar_snackbar("Por favor ingresa tu contraseña.", exito=False)
            return

        print("CONTRASEÑA ACTUAL:", confirmar_contraseña)

        respuesta = deshabilitar_usuario(page, confirmar_contraseña)

        if not respuesta.get("success"):
            print("Error:", respuesta.get("message"))

    def capturar_contraseña(e):
        confirmar_contraseña = confirmar_contraseña_field.value.strip() if confirmar_contraseña_field.value else None

        if not confirmar_contraseña:
            mostrar_snackbar("Por favor ingresa tu contraseña.", exito=False)
            return

        print("CONTRASEÑA ACTUAL:", confirmar_contraseña)

        respuesta = deshabilitar_usuario(page, confirmar_contraseña)

        if not respuesta.get("success"):
            print("Error:", respuesta.get("message"))

    # INICIALIZAR VARIABLE

    confirmar_contraseña_field = ft.TextField( password=True, can_reveal_password=True,border_radius=8, bgcolor="#E0E0E0", width=600)


    # ---------------------- CONTENIDO ----------------------
    contenido = ft.Row(
        alignment="center",
        controls=[
            ft.Container(
                width=600,
                margin=ft.margin.only(top=80),
                content=ft.Column(
                    spacing=25,
                    horizontal_alignment="start",
                    controls=[
                        ft.Text("Deshabilitar cuenta", size=26, weight="bold", color=PRIMARY_COLOR, font_family="Oswald"),
                        ft.Text(
                            "Esta acción es permanente y no se puede deshacer.\n"
                            "Toda tu información se eliminará de forma irreversible.\n"
                            "No podrás volver a iniciar sesión con esta cuenta.",
                            size=16,
                            color="black",
                            font_family="Oswald"
                        ),
                        ft.Text("Confirmar contraseña", size=18, color="black", font_family="Oswald"),
                        confirmar_contraseña_field,
                        ft.Row(
                            alignment="start",
                            spacing=20,
                            controls=[
                                ft.ElevatedButton(
                                    "Cancelar",
                                    bgcolor="#F5F5F5",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=30),
                                        side=ft.BorderSide(width=2, color="#D9D9D9"),
                                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                                        text_style=ft.TextStyle(font_family="Oswald", size=18),
                                    ),
                                    on_click=lambda e: (page.clean(), config_cuenta.main(page))
                                ),
                                ft.ElevatedButton(
                                    "Deshabilitar cuenta",
                                    bgcolor="#F5F5F5",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=30),
                                        side=ft.BorderSide(width=2, color=PRIMARY_COLOR),
                                        padding=ft.padding.symmetric(horizontal=30, vertical=12),
                                        text_style=ft.TextStyle(font_family="Oswald", size=18),
                                    ),
                                    on_click=capturar_contraseña
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
                ft.Container(expand=True)
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
