import flet as ft
from nltk.sem.chat80 import borders
import publicaciones
import crearADMIN
from flet import Icons, Colors
import datetime
from CaliTrabaja.Views import usuarios


def main(page: ft.Page):
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    DESCRIPTION_BG = "#EEEEEE"
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "#DDDDDD"
    TEXT_COLOR = "#333333"
    DESCRIPTION_TEXT_COLOR = ft.Colors.BLACK54

    page.title = "CaliTrabaja - Reportes"
    page.window_maximized = True
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 20

    selected_date_text = ft.Text("Sin seleccionar", size=12, color=Colors.BLACK45)

    def update_date_text(e):
        selected_date_text.value = f"Seleccionado: {e.control.value}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=update_date_text,
        first_date=datetime.date(2020, 1, 1),
        last_date=datetime.date(2030, 12, 31),
    )
    page.overlay.append(date_picker)

    def open_date_picker():
        date_picker.open = True
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
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.INFO_OUTLINE, size=28, color=TEXT_COLOR),
                            title=ft.Text("Nosotros", size=18, color=TEXT_COLOR),
                            on_click=on_drawer_item_click,
                        ),
                        ft.Container(expand=True),
                        ft.Container(
                            alignment=ft.alignment.bottom_right,
                            padding=ft.padding.only(right=10, bottom=10),
                            content=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, size=32, color=TEXT_COLOR),
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
                    ),
                ),
            ],
        ),
    )

    tabs = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Row(
            [
                ft.TextButton(
                    text="Usuarios",
                    on_click=lambda e: usuarios.main(page),
                    style=ft.ButtonStyle(
                        color=TEXT_COLOR,
                        padding=10,
                        text_style=ft.TextStyle(size=24, font_family="Oswald", weight=ft.FontWeight.BOLD),
                    ),
                ),
                ft.TextButton(
                    text="Publicaciones",
                    on_click=lambda e: publicaciones.main(page),
                    style=ft.ButtonStyle(
                        color=TEXT_COLOR,
                        padding=10,
                        text_style=ft.TextStyle(size=24, font_family="Oswald", weight=ft.FontWeight.BOLD),
                    ),
                ),
                ft.TextButton(
                    text="Reportes",
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        padding=10,
                        text_style=ft.TextStyle(size=24, font_family="Oswald", weight=ft.FontWeight.BOLD),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
        # Configuracion
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=25,
        padding=5,
        # Re-cuadro
        margin=ft.margin.only(top=5, bottom=20, left=250, right=250),

    )

    filtros = ft.Container(
        content=ft.Column([
            ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=Colors.BLACK54),
            ft.Row([

                ft.Text("ID Reporte", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                ft.TextField(width=120, height=35, text_size=12, border_radius=5),

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.Text("Fecha Reporte", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                ft.IconButton(
                    icon=ft.Icons.CALENDAR_MONTH,
                    tooltip="Seleccionar fecha",
                    on_click=lambda e: open_date_picker(),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            selected_date_text,
            ft.Row([
                ft.Text("ID Usuario", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                ft.TextField(width=120, height=35, text_size=12, border_radius=5)

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
            spacing=8,
        ),
        padding=12,
        bgcolor=CARD_BACKGROUND,
        height=250,
        width=260,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    def tarjeta_reporte(de, para, id_reporte, full_description):
        display_description = full_description.split(' ... ')[0] if ' ... ' in full_description else full_description
        has_more = ' ... ' in full_description

        def get_stars(rating):
            return ft.Row(
                [
                    ft.Icon(
                        Icons.STAR if i < rating else Icons.STAR_BORDER,
                        color=PRIMARY_COLOR,
                        size=16
                    ) for i in range(5)
                ],
                spacing=1
            )

        return ft.Container(
            bgcolor=CARD_BACKGROUND,
            padding=20,
            content=ft.Column([
                ft.Row([
                    ft.Text(f"De: {de}", color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Text("ID ", color=Colors.BLACK45, size=12),
                        ft.Text(f"#{id_reporte}", color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD, size=12),
                        ft.PopupMenuButton(
                            icon=Icons.MORE_HORIZ,
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
                    content=ft.Column([
                        ft.Text(display_description, color=TEXT_COLOR, size=14, max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text("Ver más", color=Colors.BLUE, size=12, italic=True) if has_more else ft.Container(),
                    ], spacing=2),
                    bgcolor=DESCRIPTION_BG,
                    padding=ft.padding.all(10),
                    border_radius=5,
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Notificar Usuario",
                        bgcolor=CARD_BACKGROUND,
                        color=TEXT_COLOR,
                        style=ft.ButtonStyle(
                            padding=ft.padding.symmetric(horizontal=15, vertical=10),
                            shape=ft.RoundedRectangleBorder(radius=15),
                            side=ft.BorderSide(1, PRIMARY_COLOR))
                    ),
                    alignment=ft.alignment.center
                ),
            ], spacing=19),
            border_radius=8,
            border=ft.border.all(1, BORDER_COLOR),
            width=400,
            height=280,
        )

    reportes_demo = [
        {
            "de": "Néstor",
            "para": "Nalga Flaca",
            "id_reporte": "09",
            "full_description": "Se cree la del desierto y parece un jugo de papaya caliente JAJAJAJAJAJAA ... Ver más"
        },
        {
            "de": "Ana",
            "para": "Sol Melano",
            "id_reporte": "08",
            "full_description": "La contraté como masajista quien dice que no firei feliz."
        },
        {
            "de": "Ana",
            "para": "Sol Melano",
            "id_reporte": "08",
            "full_description": "La contraté como masajista quien dice que no firei feliz."
        },
        {
            "de": "Ana",
            "para": "Sol Melano",
            "id_reporte": "08",
            "full_description": "La contraté como masajista quien dice que no firei feliz."
        },
    ]

    tarjetas = [tarjeta_reporte(**report) for report in reportes_demo]



    VISIBLE_CARDS = 5
    start_index = 0
    tarjetas_container = ft.Row(spacing=20, expand=True, wrap=False, scroll=ft.ScrollMode.ADAPTIVE)

    def actualizar_tarjetas():
        tarjetas_container.controls = [tarjetas[(start_index + i) % len(tarjetas)] for i in range(VISIBLE_CARDS)]
        page.update()

    def siguiente(e):
        nonlocal start_index
        start_index = (start_index + VISIBLE_CARDS) % len(tarjetas)
        actualizar_tarjetas()

    def anterior(e):
        nonlocal start_index
        start_index = (start_index - VISIBLE_CARDS + len(tarjetas)) % len(tarjetas)
        actualizar_tarjetas()

    actualizar_tarjetas()

    publicaciones_list_container = ft.Container(
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "Todos los reportes",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=PRIMARY_COLOR,
                    ),
                    padding=ft.padding.only(left=-240),
                ),
                ft.Container(content=tarjetas_container, padding=30, margin=0),
                ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, on_click=anterior, icon_size=40,
                                  icon_color=PRIMARY_COLOR),
                    ft.IconButton(icon=ft.Icons.ARROW_FORWARD_IOS, on_click=siguiente, icon_size=40,
                                  icon_color=PRIMARY_COLOR),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=520),
                ft.Text(f"Total de reportes: {VISIBLE_CARDS}/{len(reportes_demo)}", size=14,
                        color=TEXT_COLOR,
                        text_align=ft.TextAlign.CENTER),

            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        expand=True,
        padding=ft.padding.only(left=0, right=0, top=12, bottom=0)
    )

    main_content = ft.Row(
        [
            ft.Container(
                content=ft.Column([filtros]),
                padding=ft.padding.only(top=85),
            ),
            ft.Container(
                content=publicaciones_list_container,
                expand=True,
                padding=ft.padding.only(left=20, top=0),
            ),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=20,
    )

    page.add(header, tabs, main_content)


if __name__ == "__main__":
    ft.app(target=main)
