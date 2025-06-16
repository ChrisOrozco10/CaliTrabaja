import flet as ft
import reportes
import usuarios
import crearADMIN
from datetime import datetime


def main(page: ft.Page, seleccionar_fecha=None):
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    BORDER_COLOR = "#DDDDDD"
    CARD_BACKGROUND = "#FFFFFF"
    BACKGROUND_COLOR = "#FAFAFA"

    page.title = "CaliTrabaja - Publicaciones"
    page.window_maximized = True
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 20

    def open_drawer(e):
        page.drawer.open = True
        page.update()

    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        if isinstance(e.control.title, ft.Text):
            title = e.control.title.value
            if title == "Crear Usuario Administrador":
                crearADMIN.main(page)
            elif title == "Inicio":
                usuarios.main(page)
            elif title == "Configuración de cuenta":
                reportes.main(page)
        close_drawer(e)

    # Campo que mostrará la fecha seleccionada
    fecha_field = ft.TextField(
        width=120,
        read_only=True,
        hint_text="Elegir fecha",
        text_size=12,
    )

    # Campo donde se mostrará la fecha seleccionada
    fecha_field = ft.TextField(
        width=120,
        read_only=True,
        hint_text="Elegir fecha",
        text_size=12,
    )

    # Campo que muestra la fecha seleccionada
    fecha_field = ft.TextField(
        width=120,
        read_only=True,
        hint_text="Elegir fecha",
        text_size=12,
    )
    # Campo donde se mostrará la fecha seleccionada
    fecha_field = ft.TextField(
        width=120,
        read_only=True,
        hint_text="Elegir fecha",
        text_size=12,
    )

    # DatePicker que se abre desde botón y actualiza el campo
    fecha_picker = ft.DatePicker(
        on_change=lambda e: (
            setattr(fecha_field, "value", e.control.value.strftime("%Y-%m-%d")),
            fecha_field.update()
        ),
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
    )

    # Botón que abre el calendario
    btn_fecha = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        icon_color="#2FBDB3",
        tooltip="Seleccionar fecha",
        on_click=lambda e: fecha_picker.pick_date()
    )

    # Añadir el date picker al overlay
    page.overlay.append(fecha_picker)

    # Drawer
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
                            leading=ft.Icon(ft.Icons.HOME_OUTLINED, size=28, color=ft.Colors.BLACK),
                            title=ft.Text("Inicio", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=28, color=ft.Colors.BLACK),
                            title=ft.Text("Configuración de cuenta", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=28, color=ft.Colors.BLACK),
                            title=ft.Text("Crear Usuario Administrador", size=18, color=ft.Colors.BLACK),
                            on_click=on_drawer_item_click,
                        ),
                    ],
                ),
            )
        ],
    )

    # Header
    header = ft.Container(
        bgcolor="#F8F8F8",
        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            spacing=20,
            controls=[
                ft.IconButton(icon=ft.Icons.MENU, icon_color="#000000", on_click=open_drawer),
                ft.Row(
                    spacing=10,
                    controls=[
                        ft.Image(src="../img/logo.png", width=32, height=32),
                        ft.Text("Cali", color=PRIMARY_COLOR, size=20),
                        ft.Text("Trabaja", color="#000000", size=20),
                    ],
                ),
            ],
        ),
    )

    # Tabs
    tabs = ft.Container(
        content=ft.Row([
            ft.TextButton("Usuarios", on_click=lambda e: usuarios.main(page), style=ft.ButtonStyle(color=TEXT_COLOR)),
            ft.TextButton("Publicaciones", style=ft.ButtonStyle(color=PRIMARY_COLOR)),
            ft.TextButton("Reportes", on_click=lambda e: reportes.main(page), style=ft.ButtonStyle(color=TEXT_COLOR)),
        ]),
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=30,
        padding=ft.padding.only(left=20, right=20),
        margin=ft.margin.only(top=10, bottom=20),
    )

    # Filtros
    filtros = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=TEXT_COLOR),

                ft.Row([
                    ft.Text("ID publicación", expand=True, color=TEXT_COLOR, size=12),
                    ft.TextField(width=120, text_size=12),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Text("Fecha publicación", expand=True, color=TEXT_COLOR, size=12),
                    fecha_field
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Text("Categoría", expand=True, color=TEXT_COLOR, size=12),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Electricista"),
                            ft.dropdown.Option("Plomero"),
                            ft.dropdown.Option("Carpintero"),
                            ft.dropdown.Option("Jardinero"),
                            ft.dropdown.Option("Cerrajero"),
                            ft.dropdown.Option("Pintor"),
                            ft.dropdown.Option("Niñera"),
                            ft.dropdown.Option("Sistemas"),
                            ft.dropdown.Option("Técnico automotriz"),
                            ft.dropdown.Option("Gasodomésticos"),
                        ],
                        text_size=12,
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Text("Premium", expand=True, color=TEXT_COLOR, size=12),
                    ft.Checkbox()
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
            spacing=10,
        ),
        padding=12,
        bgcolor=CARD_BACKGROUND,
        width=250,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    # Publicaciones (donde estaban los usuarios)
    def tarjeta_publicacion(nombre, categoria):
        return ft.Container(
            bgcolor=CARD_BACKGROUND,
            padding=16,
            content=ft.Column([
                ft.Text(f"Publicado por: {nombre}", weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                ft.Text(f"Categoría: {categoria}", color=TEXT_COLOR),
                ft.Container(height=10),
                ft.ElevatedButton(
                    text="Contactar experto",
                    bgcolor=PRIMARY_COLOR,
                    color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
                )
            ]),
            border=ft.border.all(1, BORDER_COLOR),
            border_radius=10,
            width=350,
        )

    lista_publicaciones = ft.ListView(
        controls=[
            tarjeta_publicacion("Juan Pérez", "Electricista"),
            tarjeta_publicacion("Ana Gómez", "Niñera"),
        ],
        spacing=15,
        auto_scroll=False,
    )

    main_content = ft.Row([
        filtros,
        ft.Container(
            content=lista_publicaciones,
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
