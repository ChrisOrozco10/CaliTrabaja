import flet as ft
import crearADMIN
import usuarios
import publicaciones
from flet import Icons, Colors

def main(page: ft.Page):
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")  # Fuente Oswald por defecto
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "#DDDDDD"
    TEXT_COLOR = "#333333"
    DESCRIPTION_BG = "#EEEEEE"

    page.title = "CaliTrabaja - Reportes"
    page.window_maximized = True
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 20

    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        if isinstance(e.control.title, ft.Text):
            title = e.control.title.value
            if title == "Crear Usuario Administrador":
                crearADMIN.main(page)
        page.drawer.open = False
        page.update()

    def open_drawer(e):
        page.drawer.open = True
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
                            leading=ft.Icon(
                                ft.Icons.HOME_OUTLINED, size=28, color=ft.Colors.BLACK
                            ),
                            title=ft.Text("Inicio", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.SETTINGS_OUTLINED, size=28, color=ft.Colors.BLACK
                            ),
                            title=ft.Text("Configuración de cuenta", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.PERSON_ADD_OUTLINED, size=28, color=ft.Colors.BLACK
                            ),
                            title=ft.Text("Crear Usuario Administrador", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(
                                ft.Icons.INFO_OUTLINE, size=28, color=ft.Colors.BLACK
                            ),
                            title=ft.Text("Nosotros", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.only(right=10, bottom=10),
                            content=ft.Icon(
                                ft.Icons.WB_SUNNY_OUTLINED, size=32, color=ft.Colors.BLACK
                            ),
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
                ft.IconButton(
                    icon=ft.Icons.MENU, icon_color="#000000", on_click=open_drawer
                ),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Image(src="../img/logo.png", width=32, height=32),
                        ft.Text("Cali", color=PRIMARY_COLOR, size=20, font_family="Oswald"),
                        ft.Text("Trabaja", color="#000000", size=20, font_family="Oswald"),
                    ],
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center_right,
                    content=ft.ElevatedButton(
                        "Cerrar Sesion",
                        bgcolor="#3EAEB1",
                        color="white",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=30),
                            padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
                        ),
                    ),
                ),
            ],
        ),
    )

    tabs = ft.Container(
        content=ft.Row([
            ft.TextButton(
                text="Usuarios",
                on_click=lambda e: usuarios.main(page),  # 👈 ejecuta solo al hacer clic
                style=ft.ButtonStyle(color=TEXT_COLOR)
            ),
            ft.TextButton(
                text="Publicaciones",
                on_click=lambda e: publicaciones.main(page),
                style=ft.ButtonStyle(color=TEXT_COLOR)
            ),
            ft.TextButton(
                text="Reportes",
                style=ft.ButtonStyle(color=PRIMARY_COLOR)
            ),
        ]),
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=30,
        padding=ft.padding.only(left=20, right=20),
        margin=ft.margin.only(top=10, bottom=20),
    )

    filtros = ft.Container(
        content=ft.Column([
            ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=Colors.BLACK54),
            ft.Row([
                ft.Text("ID Reporte", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                ft.Checkbox()
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Text("Fecha Reporte", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                ft.Checkbox()
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Text("ID Usuario", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                ft.Checkbox()
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], spacing=15),
        padding=20,
        bgcolor=CARD_BACKGROUND,
        width=250,
        height=350,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    def tarjeta_reporte(de, para, id, descripcion):
        return ft.Container(
            bgcolor=CARD_BACKGROUND,
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text(f"De: {de}", color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Text("ID ", color=Colors.BLACK45),
                        ft.Text(f"#{id}", color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
                        ft.PopupMenuButton(
                            icon=Icons.MORE_VERT,
                            items=[
                                ft.PopupMenuItem(text="Ver perfil"),
                                ft.PopupMenuItem(text="Eliminar Reporte"),
                                ft.PopupMenuItem(text="Notificar Problema"),
                            ]
                        ),
                    ]),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(f"Para: {para}", weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                ft.Container(
                    content=ft.Text(descripcion, color=TEXT_COLOR),
                    bgcolor=DESCRIPTION_BG,
                    padding=10,
                    border_radius=5,
                ),
                ft.Row([
                    ft.ElevatedButton(
                        text="Notificar Usuario",
                        bgcolor=PRIMARY_COLOR,
                        color=CARD_BACKGROUND,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                    ),
                    ft.OutlinedButton(
                        text="Eliminar Reporte",
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                            color=TEXT_COLOR,
                        ),
                    ),
                ], spacing=10),
            ], spacing=10),
            border_radius=8,
            border=ft.border.all(1, BORDER_COLOR),
            width=400,
        )

    reportes_container = ft.Container(
        content=ft.Column([
            ft.Text("Todos los reportes", size=20, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.ListView(
                    controls=[
                        tarjeta_reporte("Néstor", "Nalga Flaca", "09", "Descripción: Se cree la del desierto y parece un jugo de papaya caliente JAJAJAJAJAJAA ... Ver más"),
                        tarjeta_reporte("Ana", "Sol Melano", "08", "Descripción: La contraté como masajista quien dice que no firei feliz."),
                    ],
                    spacing=20,
                    horizontal=True,
                    height=300,
                ),
            ),
            ft.Text("Total reportes: 2", size=14, color=Colors.BLACK45),
        ], spacing=20),
    )

    main_content = ft.Row([
        filtros,
        ft.Container(
            content=reportes_container,
            expand=True,
            padding=ft.padding.only(left=20),
        ),
    ], expand=True, spacing=20)

    page.add(
        header,
        tabs,
        main_content,
    )

if __name__ == "__main__":
    ft.app(target=main)
