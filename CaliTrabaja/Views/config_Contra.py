import flet as ft
import inicio
import login
import crearADMIN
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api

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

    def cerrar_sesion(e):
        respuesta = cerrar_sesion_api()
        page.clean()
        login.main(page)

        if respuesta.get("success"):
            page.snack_bar = ft.SnackBar(ft.Text("Sesión cerrada correctamente."), bgcolor="green")
            page.snack_bar.open = True
            page.update()
            # Redirigir al login (si lo tienes)
            # login.main(page)
        else:
            page.snack_bar = ft.SnackBar(ft.Text(respuesta.get("message", "Error al cerrar sesión")), bgcolor="red")
            page.snack_bar.open = True
            page.update()

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
                        ft.TextField(
                            password=True, can_reveal_password=True,
                            border_radius=8, bgcolor="#E0E0E0", width=600
                        ),

                        ft.Text("Nueva contraseña", size=18, color="black", font_family="Oswald"),
                        ft.TextField(
                            password=True, can_reveal_password=True,
                            border_radius=8, bgcolor="#E0E0E0", width=600
                        ),

                        ft.Text("Repetir contraseña", size=18, color="black", font_family="Oswald"),
                        ft.TextField(
                            password=True, can_reveal_password=True,
                            border_radius=8, bgcolor="#E0E0E0", width=600
                        ),

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
                                    )
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
