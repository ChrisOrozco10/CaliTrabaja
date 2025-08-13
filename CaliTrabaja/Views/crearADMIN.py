import flet as ft
import inicio
import config_cuenta
from CaliTrabaja.API_services.registrar_admin import registrar_sesion_api
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
import login



def main(page: ft.Page):
    # ---------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    PRIMARY_COLOR = "#2FBDB3"
    page.bgcolor = "white"
    TEXT_COLOR = "#333333"
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
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

    def conceder_acceso(e):
        correo = correo_field.value.strip()
        if not correo:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor ingresa un correo."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Llamar API
        respuesta = registrar_sesion_api(correo)

        color = "green" if respuesta.get("success") else "red"
        page.snack_bar = ft.SnackBar(ft.Text(respuesta.get("message", "")), bgcolor=color)
        page.snack_bar.open = True
        page.update()

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
                            title=ft.Text("Inicio", size=18, color=TEXT_COLOR),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Configuración de cuenta", size=18, color=TEXT_COLOR),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Crear Usuario Administrador", size=18, color=TEXT_COLOR),
                            on_click=on_drawer_item_click,
                        ),
                    ],
                ),
            )
        ],
    )

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
                        on_click= cerrar_sesion
                    ),
                ),
            ],
        ),
    )

    # DECLARAR EL CAMPO FUERA DEL controls

    correo_field = ft.TextField(
        width=300,
        hint_text="Correo electrónico",
        bgcolor="#F5F5F5",
        border_color="#E0E0E0",
        text_size=14,
        content_padding=ft.padding.only(left=10, top=0, bottom=0),
        text_style=ft.TextStyle(font_family="Oswald"),
        hint_style=ft.TextStyle(font_family="Oswald"),
    )


    # ---------------------- FORMULARIO PRINCIPAL ----------------------
    main_card = ft.Container(
        width=800,
        height=400,
        padding=ft.padding.all(30),
        bgcolor="#FFFFFF",
        border_radius=ft.border_radius.all(20),
        # Sombra gris suave ‑‑ SIN bordes negros
        shadow=ft.BoxShadow(
            color="#E0E0E0",
            blur_radius=10,
            spread_radius=1,
            offset=ft.Offset(0, 5),
        ),
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Crear usuario Administrador",
                    color="#2FBDB3",
                    size=20,
                    font_family="Oswald",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=20),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("@", color="#2FBDB3", size=16, font_family="Oswald"),
                        correo_field
                    ],
                ),
                ft.Container(height=20),
                ft.Text(
                    "Esta acción le concede el acceso del área\nadministrativa al usuario seleccionado.",
                    text_align=ft.TextAlign.CENTER,
                    size=14,
                    color="#757575",
                    font_family="Oswald",
                ),
                ft.Container(height=20),
                ft.ElevatedButton(
                    text="Conceder Acceso",
                    bgcolor="#FFFFFF",
                    color="#000000",
                    on_click=conceder_acceso,
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(width=2, color="#2FBDB3"),
                        shape=ft.RoundedRectangleBorder(radius=30),
                        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
                        text_style=ft.TextStyle(font_family="Oswald"),
                    ),
                ),
            ],
        ),
    )



    # ---------------------- CENTRAR FORMULARIO ----------------------
    content = ft.Container(
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=100),
        content=main_card,
    )

    # ---------------------- AGREGAR A LA PÁGINA ----------------------
    page.add(header, content)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)

