import flet as ft
import usuarios
import login
import publicaciones
import reportes
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
    BACKGROUND_COLOR = "#FAFAFA"
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
            if title == "Configuración de cuenta":
                config_cuenta.main(page)
            if title == "Crear Usuario Administrador":
                crearADMIN.main(page)
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
                            title=ft.Text("Inicio", size=18, color=TEXT_COLOR, font_family= "Oswald"),
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

    # ---------------------- TARJETAS ----------------------
    def tarjeta(titulo, subtitulo, accion):
        return ft.Container(
            padding=ft.padding.all(30),
            width=180,
            height=180,
            bgcolor=CARD_BACKGROUND,
            border=ft.border.all(1, PRIMARY_COLOR),
            border_radius=ft.border_radius.all(12),
            alignment=ft.alignment.center,
            on_click=lambda e: accion(),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR, font_family="Oswald"),
                    ft.Text(subtitulo, size=14, color="#000000", text_align=ft.TextAlign.CENTER, font_family="Oswald"),
                ]
            )
        )

    main_card = ft.Container(
        width=1000,
        height=450,
        padding=ft.padding.all(50),
        bgcolor="#FFFFFF",
        border= ft.border.all(1,TEXT_COLOR),
        border_radius=ft.border_radius.all(15),
        shadow=ft.BoxShadow(
            color="#D3D3D3",
            blur_radius=15,
            spread_radius=1,
            offset=ft.Offset(0, 5),
        ),
        content=ft.Column(
            spacing=40,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Bienvenidos !", size=36, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR, font_family="Oswald"),
                ft.Row(
                    spacing=40,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        tarjeta("Usuario", "Busqueda de Usuarios", lambda: usuarios.main(page)),
                        tarjeta("Publicacion", "Busqueda de Publicaciones", lambda: publicaciones.main(page)),
                        tarjeta("Reporte", "Busqueda de Reportes", lambda: reportes.main(page))
                    ]
                )
            ]
        )
    )

    content = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=main_card,
    )

    # ---------------------- AGREGAR A LA PÁGINA ----------------------
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(height=80),
                content
            ]
        )
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
