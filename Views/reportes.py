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
    page.theme = ft.Theme(font_family="Oswald")
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "#DDDDDD"
    TEXT_COLOR = "#333333"
    DESCRIPTION_BG = "#EEEEEE"

    page.title = "CaliTrabaja - Reportes"
    page.window_maximized = True
    page.bgcolor = BACKGROUND_COLOR
    # Keep page padding minimal at the top for maximum upward movement
    page.padding = 20

    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        if isinstance(e.control.title, ft.Text):
            title = e.control.title.value
            if title == "Crear Usuario Administrador":
                crearADMIN.main(page)
            elif title == "Inicio":  # <--- AGREGADO: Manejar la opción "Inicio"
                usuarios.main(page)  # <--- Llamar a la función main del módulo usuarios (usuarios.py)
        page.drawer.open = False
        page.update()

    def open_drawer(e):
        page.drawer.open = True
        page.update()

        # --- Drawer ---

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
                            content=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, size=32),
                        ),
                    ],
                ),
            )
        ],
    )

    # --- Header ---
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
                        ft.Text("Cali", color=PRIMARY_COLOR, size=20, font_family="Oswald"),
                        ft.Text("Trabaja", color="#000000", size=20, font_family="Oswald"),
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
        content=ft.Row([
            ft.TextButton(
                text="Usuarios",
                on_click=lambda e: usuarios.main(page),
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
        # Crucial change: Reduce bottom margin to pull content up
        margin=ft.margin.only(top=10, bottom=5), # Reduced from 20 to 5
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

    def tarjeta_reporte(de, para, id_reporte, full_description):
        display_description = full_description.split(' ... ')[0] if ' ... ' in full_description else full_description
        has_more = ' ... ' in full_description

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
                    content=ft.Column([
                        ft.Text(display_description, color=TEXT_COLOR, size=14, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text("Ver más", color=Colors.BLUE, size=12, italic=True) if has_more else ft.Container(),
                    ], spacing=2),
                    bgcolor=DESCRIPTION_BG,
                    padding=ft.padding.all(10),
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
                            side=ft.BorderSide(1, BORDER_COLOR)
                        ),
                    ),
                ], spacing=10),
            ], spacing=10),
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
    ]

    report_cards = [tarjeta_reporte(**report) for report in reportes_demo]

    reportes_container = ft.Container(
        content=ft.Column([
            ft.Text("Todos los reportes", size=22, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
            ft.Row(
                report_cards,
                spacing=20,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                height=300,
            ),
            # This text now represents the total at the bottom
            ft.Text(f"Total reportes: {len(reportes_demo)}", size=14, color=Colors.BLACK45),
        ],
        spacing=10, # Adjusted spacing within this column. You might need to fine-tune this.
        horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        expand=True,
        # Removed explicit top padding here, it should now be controlled by parent and internal spacing
        padding=ft.padding.only(left=0, right=0, top=0, bottom=0)
    )

    main_content = ft.Row(
        [
            filtros,
            ft.Container(
                content=reportes_container,
                expand=True,
                # Set padding to zero here or a minimal value to pull content up
                padding=ft.padding.only(left=20, top=0, right=0, bottom=0),
            ),
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=20,
    )

    page.add(
        header,
        tabs,
        main_content, # No margin for main_content to allow it to stick to tabs
    )

if __name__ == "__main__":
    ft.app(target=main)