import flet as ft
import crearADMIN
import inicio
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
import login

def main(page: ft.Page):
    # Configuración general
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Perfil Experto - CaliTrabaja"
    page.bgcolor = "white"
    page.scroll = "adaptive"

    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    COLOR_BORDE = "#cfcfcf"

    # -------------------- Drawer ------------------------------------------
    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        title = e.control.title.value if isinstance(e.control.title, ft.Text) else ""
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
                        ft.Container(expand=True),
                    ],
                ),
            )
        ],
    )
    # -------------------- Encabezado --------------------------------------
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
                        ft.Text("Cali", size=40, font_family="Oswald", color=PRIMARY_COLOR),
                        ft.Text("Trabaja", size=40, font_family="Oswald", color="#000000"),
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
                    )
                ),
            ],
        ),
    )

    # TÍTULO
    title = ft.Container(
        content=ft.Text("Perfil Experto", size=26, weight="bold", color=PRIMARY_COLOR),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=15)
    )

    # PERFIL IZQUIERDA
    profile_image = ft.Container(
        content=ft.Icon(name="person", size=60, color=PRIMARY_COLOR),
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=100,
        padding=20
    )
    stars = ft.Row(
        [ft.Icon(name="star", color=PRIMARY_COLOR, size=20) for _ in range(5)],
        alignment="center"
    )

    left_column = ft.Column(
        [
            ft.Text("Angie Calderon", size=18, weight="bold", color=TEXT_COLOR),
            profile_image,
            stars
        ],
        horizontal_alignment="center",
        spacing=10
    )

    # DESCRIPCIÓN Y EXPERIENCIA
    description = ft.Text(
        "Apasionada por el fitness, te ayudo a alcanzar tus metas de salud y fuerza "
        "con planes de entrenamiento personalizados. Mi enfoque combina disciplina "
        "y motivación para que logres tu mejor versión.",
        size=13, color=TEXT_COLOR
    )

    experience = ft.Column([
        ft.Text("Experiencia", size=14,color=TEXT_COLOR, weight="bold"),
        ft.Text("Coaching", color=TEXT_COLOR),
        ft.Text("Smart Fit", color=TEXT_COLOR),
        ft.Text("enero 2023 - septiembre 2024", size=12, color=TEXT_COLOR),
    ], spacing=3)

    studies = ft.Column([
        ft.Text("Mis estudios", size=14, weight="bold", color=TEXT_COLOR),
        ft.Text("Técnico en actividad física", color=TEXT_COLOR),
        ft.Text("Servicio nacional de aprendizaje", color=TEXT_COLOR ),
        ft.Text("julio 2022 - diciembre 2022", size=12, color=TEXT_COLOR)
    ], spacing=3)

    center_column = ft.Column(
        [
            ft.Text("Descripción:", size=14, weight="bold", color=TEXT_COLOR),
            description,
            ft.ResponsiveRow([
                ft.Column([experience], col={"xs": 12, "sm": 6}),
                ft.Column([studies], col={"xs": 12, "sm": 6}),
            ])
        ],
        spacing=12
    )

    # CUADRO DE IDIOMAS Y APTITUDES
    def cuadro_titulo(titulo, items):
        return ft.Container(
            content=ft.Column(
                [ft.Text(titulo, size=14, weight="bold", color=TEXT_COLOR)] +
                [ft.Row([ft.Icon(name="check", color=PRIMARY_COLOR, size=18), ft.Text(txt, color=TEXT_COLOR)]) for txt in items],
                spacing=5
            ),
            border=ft.border.all(1, COLOR_BORDE),
            border_radius=10,
            padding=15
        )

    idiomas = cuadro_titulo("Idiomas", ["Español", "Inglés"])
    aptitudes = cuadro_titulo("Aptitudes", ["Liderazgo", "Comunicación efectiva"])

    right_column = ft.Column([idiomas, aptitudes], spacing=15)

    # CARD PRINCIPAL
    main_card = ft.Container(
        content=ft.ResponsiveRow([
            ft.Column([left_column], col={"xs": 12, "sm": 3}),
            ft.Column([center_column], col={"xs": 12, "sm": 6}),
            ft.Column([right_column], col={"xs": 12, "sm": 3}),
        ], alignment="spaceBetween"),
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=10,
        padding=80
    )

    # PÁGINA
    page.add(
        header,
        title,
        ft.Container(content=main_card, padding=ft.padding.all(10))
    )


ft.app(target=main)