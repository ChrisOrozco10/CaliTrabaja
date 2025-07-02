import flet as ft
import reportes
import crearADMIN
from flet import Icons
from CaliTrabaja.Views import publicaciones


def main(page: ft.Page):
    # -------------------- Tema y colores ----------------------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")

    PRIMARY_COLOR    = "#2FBDB3"     # ← Color turquesa (flechas y otros elementos)
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND  = "#FFFFFF"
    BORDER_COLOR     = "#DDDDDD"
    TEXT_COLOR       = "#333333"

    # -------------------- Config. de ventana ------------------------------
    page.title            = "CaliTrabaja - Usuarios"
    page.window_maximized = True
    page.bgcolor          = BACKGROUND_COLOR
    page.padding          = 20

    # -------------------- Drawer ------------------------------------------
    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        title = e.control.title.value if isinstance(e.control.title, ft.Text) else ""
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
                    ),
                ),
            ],
        ),
    )

    # -------------------- Pestañas ----------------------------------------
    tabs = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Usuarios",
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
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
                    on_click=lambda e: reportes.main(page),
                    style=ft.ButtonStyle(
                        color=TEXT_COLOR,
                        padding=10,
                        text_style=ft.TextStyle(size=24, font_family="Oswald", weight=ft.FontWeight.BOLD),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=25,
        padding=5,
        margin=ft.margin.only(top=5, bottom=20, left=250, right=250),
    )

    # --------------------------- Panel de filtros --------------------------
    filtros = ft.Container(
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text("Filtrar por:", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),

                # --- ID usuario ---
                ft.Row(
                    controls=[
                        ft.Text("ID usuario", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Nombre ---
                ft.Row(
                    controls=[
                        ft.Text("Nombre", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Apellido ---
                ft.Row(
                    controls=[
                        ft.Text("Apellido", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Correo ---
                ft.Row(
                    controls=[
                        ft.Text("Correo", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Rol ---
                ft.Row(
                    controls=[
                        ft.Text("Rol", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.Dropdown(
                            width=120, text_size=12, border_radius=5, value="Todos",
                            options=[ft.dropdown.Option(o) for o in ["Todos", "Experto", "Cliente"]],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Estado ---
                ft.Row(
                    controls=[
                        ft.Text("Estado", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.Dropdown(
                            width=120, text_size=12, border_radius=5, value="Todos",
                            options=[ft.dropdown.Option(o) for o in ["Todos", "Activo", "Inactivo"]],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Publicaciones ---
                ft.Row(
                    controls=[
                        ft.Text("Publicaciones", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.Dropdown(
                            width=120, text_size=12, border_radius=5, value="Todas",
                            options=[ft.dropdown.Option(o) for o in ["Todas", "Ninguna"]],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Perfiles ---
                ft.Row(
                    controls=[
                        ft.Text("Perfiles", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.Dropdown(
                            width=120, text_size=12, border_radius=5, value="Todos",
                            options=[ft.dropdown.Option(o) for o in ["Todos", "Ninguno"]],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                # --- Categorías ---
                ft.Row(
                    controls=[
                        ft.Text("Categorías", size=14, weight=ft.FontWeight.BOLD,
                                color=TEXT_COLOR, expand=True),
                        ft.Dropdown(
                            width=120, text_size=12, border_radius=5, value="Todas",
                            options=[ft.dropdown.Option(o) for o in [
                                "Todas", "Electricista", "Plomero", "Carpintero", "Jardinero",
                                "Cerrajero", "Pintor", "Niñera", "Tecnólogo en sistemas",
                                "Técnico automotriz", "Gasodomésticos"]],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
        ),
        padding=12,
        bgcolor=CARD_BACKGROUND,
        width=260,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    # -------------------- Tarjeta de usuario -------------------------------
    def tarjeta_usuario(nombre, rol, categoria, estado, fecha, correo, id_user, publicaciones, reportes, rating):
        estrellas = ft.Row([
            ft.Icon(ft.Icons.STAR if i < rating else ft.Icons.STAR_BORDER, color="#2FBDB3", size=24)
            for i in range(5)
        ])
        return ft.Container(
            bgcolor="#FFFFFF",
            padding=30,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Text(nombre, size=20, weight=ft.FontWeight.BOLD, color="#333333"),
                    estrellas,
                    ft.Text(f"Rol {rol}", size=18, color="#333333"),
                    ft.Text(f"Categoría {categoria}", size=18, color="#333333"),
                    ft.Text(f"Estado {estado}", size=18, color="#333333"),
                    ft.Text(f"Se unió el {fecha}", size=18, color="#333333"),
                    ft.Text(f"Correo {correo}", size=18, color="#333333"),
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.ElevatedButton(f"Publicaciones {publicaciones}", bgcolor="#F5F5F5", color="#333333"),
                            ft.ElevatedButton(f"Reportes {reportes}", bgcolor="#2FBDB3", color="#FFFFFF"),
                        ],
                    ),
                ],
            ),
            border_radius=10,
            border=ft.border.all(1, "#DDDDDD"),
            height=350,
            width=400,
        )

    # -------------------- Datos de ejemplo ---------------------------------
    usuarios_demo = [
        dict(nombre="Leonel Messi",   rol="Experto", categoria="Limpieza",
             estado="Activo",  fecha="20/01/2025", correo="messiento@gmail.com",
             id_user="01", publicaciones="1/2", reportes="1", rating=4),
        dict(nombre="Angie Calderón", rol="Cliente", categoria="Limpieza",
             estado="Activo",  fecha="20/01/2025", correo="angieasyavina@gmail.com",
             id_user="02", publicaciones="1/2", reportes="2", rating=5),
        dict(nombre="Carlos Pérez",   rol="Experto", categoria="Plomería",
             estado="Inactivo", fecha="15/02/2025", correo="carlosp1978@gmail.com",
             id_user="03", publicaciones="3/4", reportes="0", rating=3),
        dict(nombre="María García",   rol="Cliente", categoria="Electricidad",
             estado="Activo",  fecha="02/03/2025", correo="mariag@gmail.com",
             id_user="04", publicaciones="0",   reportes="1", rating=3),
        dict(nombre="Juan Rodríguez", rol="Experto", categoria="Jardinería",
             estado="Activo",  fecha="10/03/2025", correo="juanrdz@gmail.com",
             id_user="05", publicaciones="5/5", reportes="2", rating=2),
    ]
    tarjetas = [tarjeta_usuario(**u) for u in usuarios_demo]

    # -------------------- Carrusel -----------------------------------------
    CARD_WIDTH     = 280
    CARD_SPACING   = 20
    VISIBLE_CARDS  = 3
    CAROUSEL_WIDTH = VISIBLE_CARDS * CARD_WIDTH + (VISIBLE_CARDS - 1) * CARD_SPACING

    # Distancia exacta entre flechas (una tarjeta + su separación)
    ARROW_SPACING  = CARD_WIDTH + CARD_SPACING      # 300 px

    start_index = 0

    tarjetas_row = ft.Row(spacing=CARD_SPACING)
    tarjetas_container = ft.Container(
        width=CAROUSEL_WIDTH,
        alignment=ft.alignment.center,
        content=tarjetas_row,
    )

    def actualizar_tarjetas():
        tarjetas_row.controls = [
            tarjetas[(start_index + i) % len(tarjetas)]
            for i in range(VISIBLE_CARDS)
        ]
        page.update()

    def siguiente(e):
        nonlocal start_index
        if len(tarjetas) > VISIBLE_CARDS:
            start_index = (start_index + VISIBLE_CARDS) % len(tarjetas)
            actualizar_tarjetas()

    def anterior(e):
        nonlocal start_index
        if len(tarjetas) > VISIBLE_CARDS:
            start_index = (start_index - VISIBLE_CARDS) % len(tarjetas)
            actualizar_tarjetas()

    actualizar_tarjetas()

    # Flechas en color PRIMARY_COLOR y con icon_size 40 px
    btn_prev = ft.IconButton(
        icon=ft.Icons.ARROW_BACK_IOS_NEW,
        on_click=anterior,
        icon_size=40,
        icon_color=PRIMARY_COLOR,
    )
    btn_next = ft.IconButton(
        icon=ft.Icons.ARROW_FORWARD_IOS,
        on_click=siguiente,
        icon_size=40,
        icon_color=PRIMARY_COLOR,
    )

    # Navegación centrada y con spacing exacto
    navegacion = ft.Container(
        width=CAROUSEL_WIDTH,
        content=ft.Row(
            controls=[btn_prev, btn_next],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=ARROW_SPACING,
        ),
    )

    carrusel = ft.Column(
        controls=[tarjetas_container, navegacion],
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # -------------------- Contenido principal ------------------------------
    reportes_container = ft.Column(
        spacing=20,
        controls=[
            ft.Text("Todos los usuarios", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
            carrusel,
            ft.Text(f"Total usuarios: {len(usuarios_demo)}", size=14, color=TEXT_COLOR),
        ],
    )

    filtros_y_total = ft.Column([
        filtros,
        ft.Container(
            content=ft.Text(f"Total de usuarios: {len(usuarios_demo)}", size=14, color=TEXT_COLOR),
            padding=ft.padding.only(top=20),
            alignment=ft.alignment.center,
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    main_content = ft.ResponsiveRow([
        ft.Container(content=filtros_y_total, col={'sm': 12, 'md': 4, 'lg': 3}),
        ft.Container(content=reportes_container, col={'sm': 12, 'md': 8, 'lg': 9}),
    ], spacing=20)

    page.add(header, tabs, main_content)


if __name__ == "__main__":
    ft.app(target=main)
