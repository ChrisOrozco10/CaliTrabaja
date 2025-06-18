import flet as ft
import reportes
import crearADMIN
from flet import Icons, Colors

# Ajusta esta importación según tu estructura de carpetas real
from CaliTrabaja.Views import usuarios


def main(page: ft.Page):
    # --- Fuentes y tema ---
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")

    # --- Colores ---
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "#DDDDDD"
    TEXT_COLOR = "#333333"
    DESCRIPTION_TEXT_COLOR = ft.Colors.BLACK54

    # --- Configuración de la página ---
    page.title = "CaliTrabaja - Publicaciones"
    page.window_maximized = True
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 20

    # --- Funciones del Drawer ---
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
                            content=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, size=32, color=TEXT_COLOR),
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

    # --- Tabs estilo pills ---
    tabs = ft.Container(
        content=ft.Row([
            ft.TextButton(
                text="Usuarios",
                on_click=lambda e: usuarios.main(page),
                style=ft.ButtonStyle(color=TEXT_COLOR)
            ),
            ft.TextButton(
                text="Publicaciones",
                style=ft.ButtonStyle(color=PRIMARY_COLOR)
            ),
            ft.TextButton(
                text="Reportes",
                on_click=lambda e: reportes.main(page),
                style=ft.ButtonStyle(color=TEXT_COLOR)
            ),
        ]),
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=30,
        padding=ft.padding.only(left=20, right=20),
        margin=ft.margin.only(top=10, bottom=20),
    )

    # --- Filtros ---
    filtros = ft.Container(
        content=ft.Column(
            [
                ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=TEXT_COLOR),
                ft.Row([
                    ft.Text("ID publicación", expand=True, color=TEXT_COLOR, size=14,weight=ft.FontWeight.BOLD),
                    ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Fecha publicación", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Checkbox(width=20, height=20),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Categorías", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Todas"),
                            ft.dropdown.Option("Limpieza"),
                            ft.dropdown.Option("Belleza"),
                            ft.dropdown.Option("Reparación"), # Añadida categoría
                            ft.dropdown.Option("Diseño"),     # Añadida categoría
                        ],
                        text_size=12,
                        border_radius=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Premium", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Checkbox(width=20, height=20),
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

    # --- Componente Tarjeta de Publicación ---
    def tarjeta_publicacion(id_publicacion, nombre, profesion, descripcion, costo, categoria, calificacion_estrellas=4):
        # Función para generar estrellas
        def get_stars(rating):
            stars = []
            for i in range(5):
                if i < rating:
                    stars.append(ft.Icon(Icons.STAR, color=ft.Colors.AMBER_500, size=16))
                else:
                    stars.append(ft.Icon(Icons.STAR_BORDER, color=ft.Colors.AMBER_500, size=16))
            return ft.Row(stars, spacing=1)

        return ft.Container(
            bgcolor=CARD_BACKGROUND,
            padding=ft.padding.only(left=15, right=15, top=10, bottom=10),
            content=ft.Column(
                [
                    # Fila superior: ID y Menú de opciones
                    ft.Row(
                        [
                            ft.Text(f"ID #{id_publicacion}", size=12, color=TEXT_COLOR),
                            ft.PopupMenuButton(
                                icon=Icons.MORE_VERT,
                                items=[
                                    ft.PopupMenuItem(text="Ver perfil"),
                                    ft.PopupMenuItem(text="Eliminar y Notificar"),
                                ],
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.START
                    ),
                    # Imagen de perfil, Nombre, Calificación, Profesión
                    ft.Row(
                        [
                            ft.CircleAvatar(
                                radius=30,
                                content=ft.Icon(Icons.PERSON, size=30, color=ft.Colors.WHITE),
                                color=ft.Colors.GREY_300,
                            ),
                            ft.Column(
                                [
                                    ft.Text(nombre, size=16, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                                    get_stars(calificacion_estrellas),
                                    ft.Text(profesion, color=DESCRIPTION_TEXT_COLOR, size=13),
                                ],
                                spacing=2,
                                horizontal_alignment=ft.CrossAxisAlignment.START
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    # Descripción
                    ft.Column(
                        [
                            ft.Text("Descripción:", size=14, color=TEXT_COLOR, weight=ft.FontWeight.BOLD),
                            ft.Text(descripcion, size=12, color=DESCRIPTION_TEXT_COLOR, max_lines=3, overflow=ft.TextOverflow.ELLIPSIS),
                        ],
                        spacing=5,
                    ),
                    ft.Container(expand=True),
                    # Costo y Categoría (parte inferior izquierda)
                    ft.Column(
                        [
                            ft.Text(f"COP {costo}/hr", size=14, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                            ft.Text(f"Categoría: {categoria}", size=12, color=TEXT_COLOR),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.START
                    ),
                    # Botón "Contactar experto" (centrado)
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Contactar experto",
                            bgcolor=PRIMARY_COLOR,
                            color=CARD_BACKGROUND,
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=8),
                            ),
                            width=220,
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=10)
                    ),
                ],
                spacing=8,
            ),
            border_radius=16,
            border=ft.border.all(1, BORDER_COLOR),
            width=280,
            height=390,
        )

    # --- Datos de publicaciones de demostración ---
    publicaciones_demo = [
        {
            "id_publicacion": "34",
            "nombre": "Claudia Henao",
            "profesion": "Fotógrafa",
            "descripcion": "Con una combinación de técnica, creatividad y un profundo respeto por el instante. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "costo": "38.000",
            "categoria": "Limpieza",
            "calificacion_estrellas": 4,
        },
        {
            "id_publicacion": "45",
            "nombre": "Angela Mart",
            "profesion": "Nutricionista",
            "descripcion": "Como entrenadora personal, te ayudo a lograr tu mejor versión con planes personalizados y mucha motivación. ¡Alcanza tus metas de bienestar!",
            "costo": "45.000",
            "categoria": "Belleza",
            "calificacion_estrellas": 5,
        },
        {
            "id_publicacion": "58",
            "nombre": "Roberto Gómez",
            "profesion": "Plomero",
            "descripcion": "Especialista en reparaciones de fugas y desatascos. Trabajo rápido y eficiente, con garantía. ¡Soluciones duraderas para tu hogar!",
            "costo": "50.000",
            "categoria": "Reparación",
            "calificacion_estrellas": 3,
        },
        {
            "id_publicacion": "62",
            "nombre": "Sofía Pérez",
            "profesion": "Diseñadora Gráfica",
            "descripcion": "Diseño creativo y profesional para tus proyectos. Logos, branding, ilustraciones y más. ¡Tu visión hecha realidad!",
            "costo": "60.000",
            "categoria": "Diseño",
            "calificacion_estrellas": 4,
        },
        { # Nueva publicación 3
            "id_publicacion": "71",
            "nombre": "Carlos Restrepo",
            "profesion": "Electricista",
            "descripcion": "Servicios eléctricos residenciales y comerciales. Instalaciones, reparaciones, mantenimiento y más. ¡Seguridad y calidad garantizadas!",
            "costo": "55.000",
            "categoria": "Reparación",
            "calificacion_estrellas": 4,
        },
        { # Nueva publicación 4
            "id_publicacion": "89",
            "nombre": "María Fernanda",
            "profesion": "Asesora de Moda",
            "descripcion": "Transforma tu estilo personal. Asesoría de imagen, personal shopper y organización de armario. ¡Descubre tu mejor versión!",
            "costo": "70.000",
            "categoria": "Belleza",
            "calificacion_estrellas": 5,
        },
    ]

    # Convertir datos a tarjetas
    tarjetas = [
        tarjeta_publicacion(**p) for p in publicaciones_demo
    ]

    # --- Carrusel ---
    VISIBLE_CARDS = 3 # Ahora se verán 3 tarjetas a la vez
    start_index = 0

    tarjetas_container = ft.Row(spacing=20, expand=True, wrap=False, scroll=ft.ScrollMode.ADAPTIVE)

    def actualizar_tarjetas():
        visible = []
        total = len(tarjetas)
        if total > 0:
            # Asegura que siempre haya suficientes tarjetas para llenar la vista o se repitan
            # para el efecto de bucle.
            # Para un deslizamiento de bloque, solo tomamos las tarjetas directamente.
            for i in range(VISIBLE_CARDS):
                visible.append(tarjetas[(start_index + i) % total])
        tarjetas_container.controls = visible
        page.update()

    def siguiente(e):
        nonlocal start_index
        total = len(tarjetas)
        # Avanza VISIBLE_CARDS posiciones
        if total > VISIBLE_CARDS:
            start_index = (start_index + VISIBLE_CARDS) % total
            actualizar_tarjetas()

    def anterior(e):
        nonlocal start_index
        total = len(tarjetas)
        # Retrocede VISIBLE_CARDS posiciones
        if total > VISIBLE_CARDS:
            start_index = (start_index - VISIBLE_CARDS + total) % total
            actualizar_tarjetas()

    actualizar_tarjetas()

    btn_prev = ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, on_click=anterior, icon_size=40, icon_color=TEXT_COLOR)
    btn_next = ft.IconButton(icon=ft.Icons.ARROW_FORWARD_IOS, on_click=siguiente, icon_size=40, icon_color=TEXT_COLOR)

    carrusel = ft.Row([
        btn_prev,
        tarjetas_container,
        btn_next,
    ], spacing=10, alignment=ft.MainAxisAlignment.CENTER, expand=True)


    # --- Contenedor de publicaciones ---
    publicaciones_list_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Todas las publicaciones", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR
                ),
                carrusel,
                ft.Text(
                    f"Total publicaciones: {len(publicaciones_demo)}", size=14, color=TEXT_COLOR
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        ),
        expand=True,
        padding=ft.padding.only(left=0, right=0, top=0, bottom=0)
    )

    # --- Contenido principal ---
    main_content = ft.Row(
        [
            filtros,
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

    # --- Agregar todo a la página ---
    page.add(
        header,
        tabs,
        main_content,
    )

if __name__ == "__main__":
    ft.app(target=main)