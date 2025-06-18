import flet as ft
import reportes
import crearADMIN
from flet import Icons
from CaliTrabaja.Views import publicaciones


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

    # --- Configuración de la página ---
    page.title = "CaliTrabaja - Usuarios"
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

    # --- Tabs estilo pills ---
    tabs = ft.Container(
        content=ft.Row([
            ft.TextButton(
                text="Usuarios",
                style=ft.ButtonStyle(color=PRIMARY_COLOR)
            ),
            ft.TextButton(
                text="Publicaciones",
                on_click=lambda e: publicaciones.main(page),
                style=ft.ButtonStyle(color=TEXT_COLOR)
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

                # Campos de texto
                ft.Row([
                    ft.Text("ID usuario", expand=True, color=TEXT_COLOR, size=14,weight=ft.FontWeight.BOLD),
                    ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Text("Nombre", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Text("Apellido", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                ft.Row([
                    ft.Text("Correo", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Rol
                ft.Row([
                    ft.Text("Rol", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Experto"),
                            ft.dropdown.Option("Cliente"),
                        ],
                        text_size=12,
                        border_radius=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Estado
                ft.Row([
                    ft.Text("Estado", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Activo"),
                            ft.dropdown.Option("Inactivo"),
                        ],
                        text_size=12,
                        border_radius=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Publicaciones
                ft.Row([
                    ft.Text("Publicaciones", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Todas"),
                            ft.dropdown.Option("Ninguna"),
                        ],
                        text_size=12,
                        border_radius=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Perfiles
                ft.Row([
                    ft.Text("Perfiles", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Todos"),
                            ft.dropdown.Option("Ninguno"),
                        ],
                        text_size=12,
                        border_radius=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Categorías
                ft.Row([
                    ft.Text("Categorías", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
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
                            ft.dropdown.Option("Tecnólogo en sistemas"),
                            ft.dropdown.Option("Técnico automotriz"),
                            ft.dropdown.Option("Gasodomésticos"),
                        ],
                        text_size=12,
                        border_radius=5,
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
            spacing=8,
            # Eliminado vertical_alignment de aquí, ya que no es un argumento válido para ft.Column
        ),
        padding=12,
        bgcolor=CARD_BACKGROUND,
        height=540,
        width=260,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    # --- Componente Tarjeta de Usuario ---
    def tarjeta_usuario(nombre, rol, categoria, estado, fecha, correo, id_user, publicaciones, reportes, foto):
        return ft.Container(
            bgcolor=CARD_BACKGROUND,
            padding=20,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            # Avatar + Nombre
                            ft.Row(
                                [
                                    ft.CircleAvatar(
                                        radius=22,
                                        content=ft.Image(src="../img/avatar.png", width=48, height=48, border_radius=22,
                                                         fit=ft.ImageFit.COVER),
                                    ),

                                    ft.Text(nombre, size=16, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),
                                ],
                                spacing=12,
                            ),
                            # ID + acciones
                            ft.Row(
                                [
                                    ft.Text("ID ", size=12, color=TEXT_COLOR),
                                    ft.Text(f"#{id_user}", size=12, color=PRIMARY_COLOR, weight=ft.FontWeight.BOLD),
                                    ft.PopupMenuButton(
                                        icon=Icons.MORE_VERT,
                                        items=[
                                            ft.PopupMenuItem(text="Ver perfil"),
                                            ft.PopupMenuItem(text="Notificar Problema"),
                                            ft.PopupMenuItem(text="Deshabilitar Cuenta"),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Text(f"Rol       {rol}", color=TEXT_COLOR),
                    ft.Text(f"Categoría {categoria}", color=TEXT_COLOR),
                    ft.Text(f"Estado    {estado}", color=TEXT_COLOR),
                    ft.Text(f"Se unió el  {fecha}", color=TEXT_COLOR),
                    ft.Text(f"Correo    {correo}", color=TEXT_COLOR),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                f"Publicaciones {publicaciones}",
                                style=ft.ButtonStyle(
                                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                bgcolor="#F5F5F5",
                                color=TEXT_COLOR,
                            ),
                            ft.ElevatedButton(
                                f"Reportes {reportes}",
                                style=ft.ButtonStyle(
                                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                bgcolor=PRIMARY_COLOR,
                                color=CARD_BACKGROUND,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=8,
            ),
            border_radius=8,
            border=ft.border.all(1, BORDER_COLOR),
            height= 289,
            width=280,
        )

    # --- Datos de usuarios de demostración ---
    usuarios_demo = [
        {
            "nombre": "Leonel Messi",
            "rol": "Experto",
            "categoria": "Limpieza",
            "estado": "Activo",
            "fecha": "20 de Enero del 2025",
            "correo": "messiento@gmail.com",
            "id_user": "01",
            "publicaciones": "1/2",
            "reportes": "1",
            "foto": "https://i.pravatar.cc/150?img=11",
        },
        {
            "nombre": "Angie Calderón",
            "rol": "Cliente",
            "categoria": "Limpieza",
            "estado": "Activo",
            "fecha": "20 de Enero del 2025",
            "correo": "angieasyavina@gmail.com",
            "id_user": "02",
            "publicaciones": "1/2",
            "reportes": "2",
            "foto": "https://i.pravatar.cc/150?img=12",
        },
        {
            "nombre": "Carlos Pérez",
            "rol": "Experto",
            "categoria": "Plomería",
            "estado": "Inactivo",
            "fecha": "15 de Febrero del 2025",
            "correo": "carlosp1978@gmail.com",
            "id_user": "03",
            "publicaciones": "3/4",
            "reportes": "0",
            "foto": "https://i.pravatar.cc/150?img=13",
        },
        {
            "nombre": "María García",
            "rol": "Cliente",
            "categoria": "Electricidad",
            "estado": "Activo",
            "fecha": "02 de Marzo del 2025",
            "correo": "mariag@gmail.com",
            "id_user": "04",
            "publicaciones": "0",
            "reportes": "1",
            "foto": "https://i.pravatar.cc/150?img=14",
        },
        {
            "nombre": "Juan Rodríguez",
            "rol": "Experto",
            "categoria": "Jardinería",
            "estado": "Activo",
            "fecha": "10 de Marzo del 2025",
            "correo": "juanrdz@gmail.com",
            "id_user": "05",
            "publicaciones": "5/5",
            "reportes": "2",
            "foto": "https://i.pravatar.cc/150?img=15",
        },
    ]

    # Convertir datos a tarjetas
    tarjetas = [
        tarjeta_usuario(**u) for u in usuarios_demo
    ]

    # --- Carrusel ---
    VISIBLE_CARDS = 3  # número de tarjetas visibles a la vez
    start_index = 0

    tarjetas_container = ft.Row(spacing=20, expand=True)

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


    # --- Contenedor de reportes ---
    reportes_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Todos los usuarios", size=22, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR
                ),
                carrusel,
                ft.Text(
                    f"Total usuarios: {len(usuarios_demo)}", size=14, color=TEXT_COLOR
                ),
            ],
            spacing=20,
        ),
    )

    # --- Contenido principal ---
    main_content = ft.Row(
        [
            filtros,
            ft.Container(
                content=reportes_container,
                expand=True,
                padding=ft.padding.only(left=20),
            ),
        ],
        expand=True,
        spacing=20,
        vertical_alignment=ft.CrossAxisAlignment.START # Asegura que todo el contenido del Row se alinee arriba
    )

    # --- Agregar todo a la página ---
    page.add(
        header,
        tabs,
        main_content,
    )

if __name__ == "__main__":
    ft.app(target=main)