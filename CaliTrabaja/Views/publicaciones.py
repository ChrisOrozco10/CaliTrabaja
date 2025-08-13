import flet as ft
import reportes
import crearADMIN
from flet import Icons, Colors
import datetime
import usuarios
import login
import inicio
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api

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

    page.title = "CaliTrabaja - Publicaciones"
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
                    ],
                ),
            )
        ],
    )

    # -------------------- Modal de Confirmación ---------------------------
    dialog_title = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    dialog_description = ft.Text("", size=16)
    dialog_textfield = ft.TextField(hint_text="Descripción...", border_radius=10, multiline=True, height=80)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=dialog_title,
        content=ft.Container(
            height=110,  # ← AQUÍ MODIFICAS EL ALTO DEL MODAL
            content=ft.Column(
                spacing=15,
                controls=[
                    dialog_description,
                    dialog_textfield,
                ],
            ),
        ),
        actions=[
            ft.ElevatedButton(
                "Aceptar",
                color=TEXT_COLOR,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(width=2, color="#2FBDB3"),
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                on_click=lambda e: cerrar_dialogo()
            ),
            ft.ElevatedButton(
                "Cancelar",
                color=TEXT_COLOR,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(width=2, color="#D9D9D9"),
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                on_click=lambda e: cerrar_dialogo()
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # === FUNCIÓN PARA CERRAR EL DIALOGO ===
    def cerrar_dialogo():
        confirm_dialog.open = False
        page.update()

    def abrir_confirmacion(nombre, accion, id_usuario):
        dialog_title.value = f"¿Seguro que deseas {accion}?"
        dialog_description.value = f"Acción sobre ID #{id_usuario} ({nombre})"
        dialog_textfield.value = ""
        confirm_dialog.open = True
        page.dialog = confirm_dialog
        page.update()

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
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
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
        #Configuracion
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=25,
        padding=5,
        #Re-cuadro
        margin=ft.margin.only(top=5, bottom=20, left=250, right=250),

    )

    filtros = ft.Container(
        content=ft.Column(
            [
                ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=TEXT_COLOR),
                ft.Row([
                    ft.Text("ID publicación", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.TextField(width=120, height=35, text_size=12, border_radius=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Fecha Reporte", weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                    ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, tooltip="Seleccionar fecha", on_click=lambda e: open_date_picker()),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Categorías", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        width=120,
                        options=[
                            ft.dropdown.Option("Todas"),
                            ft.dropdown.Option("Limpieza"),
                            ft.dropdown.Option("Belleza"),
                            ft.dropdown.Option("Reparación"),
                            ft.dropdown.Option("Diseño"),
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

    def tarjeta_publicacion(id_publicacion, nombre, profesion, descripcion, costo, categoria, calificacion_estrellas=4):
        def get_stars(rating):
            return ft.Row(
                [
                    ft.Icon(
                        name=ft.Icons.STAR if i < rating else ft.Icons.STAR_BORDER,
                        color="#2FBDB3",
                        size=16
                    ) for i in range(5)
                ],
                spacing=1
            )

        menu_desplegable = ft.PopupMenuButton(
            bgcolor="#FFFFFF",
            icon=ft.Icons.MORE_HORIZ,
            icon_color="#333333",
            items=[
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.PERSON, color="#333333", size=20),
                            ft.Text("Ver perfil", color="#333333"),
                        ],
                        spacing=10,
                    ),
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.REPORT_PROBLEM, color="#333333", size=20),
                            ft.Text("Notificar Problema", color="#333333"),
                        ],
                        spacing=10,
                    ),
                    on_click=lambda e: abrir_confirmacion(nombre, "notificar un problema", id_publicacion)
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.BLOCK, color="#333333", size=20),
                            ft.Text("Eliminar Publicacion", color="#333333"),
                        ],
                        spacing=10,
                    ),
                    on_click=lambda e: abrir_confirmacion(nombre, "Eliminar la publicacion", id_publicacion)
                ),
            ],
        )

        return ft.Container(
            bgcolor="#FFFFFF",
            padding=ft.padding.only(left=15, right=15, top=10, bottom=10),
            content=ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Text(f"ID #{id_publicacion}", size=12, color="#333333"),
                            menu_desplegable,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.CircleAvatar(
                                radius=30,
                                content=ft.Icon(ft.Icons.PERSON, size=30, color=ft.Colors.WHITE),
                                color=ft.Colors.GREY_300
                            ),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(nombre, size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                                    get_stars(calificacion_estrellas),
                                    ft.Text(profesion, color="#777777", size=13),
                                ]
                            ),
                        ]
                    ),

                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text("Descripción:", size=14, color="#333333", weight=ft.FontWeight.BOLD),
                            ft.Text(descripcion, size=12, color="#777777", max_lines=3,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                        ]
                    ),

                    ft.Container(expand=True),

                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(f"COP {costo}/hr", size=14, weight=ft.FontWeight.BOLD, color="#777777"),
                            ft.Text(f"Categoría: {categoria}", size=12, color="#333333"),
                        ]
                    ),

                    ft.Container(
                        content=ft.ElevatedButton(
                            "Contactar experto",
                            bgcolor="#FFFFFF",
                            color="#333333",
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=20),
                                side=ft.BorderSide(1, "#2FBDB3"),
                            ),
                            width=220
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=10)
                    ),
                ],
                spacing=8,
            ),
            border_radius=16,
            border=ft.border.all(1, "#DDDDDD"),
            width=280,
            height=390,
        )

    publicaciones_demo = [
        {
            "id_publicacion": "34",
            "nombre": "Claudia Henao",
            "profesion": "Fotógrafa",
            "descripcion": "Con una combinación de técnica, creatividad y un profundo respeto por el instante. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "costo": "38.000",
            "categoria": "Limpieza",
            "calificacion_estrellas": 3,
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
        {
            "id_publicacion": "71",
            "nombre": "Carlos Restrepo",
            "profesion": "Electricista",
            "descripcion": "Servicios eléctricos residenciales y comerciales. Instalaciones, reparaciones, mantenimiento y más. ¡Seguridad y calidad garantizadas!",
            "costo": "55.000",
            "categoria": "Reparación",
            "calificacion_estrellas": 4,
        },
        {
            "id_publicacion": "89",
            "nombre": "María Fernanda",
            "profesion": "Asesora de Moda",
            "descripcion": "Transforma tu estilo personal. Asesoría de imagen, personal shopper y organización de armario. ¡Descubre tu mejor versión!",
            "costo": "70.000",
            "categoria": "Belleza",
            "calificacion_estrellas": 5,
        },
    ]

    tarjetas = [tarjeta_publicacion(**p) for p in publicaciones_demo]

    VISIBLE_CARDS = 5
    start_index = 0
    tarjetas_container = ft.Row(spacing=20, expand=True, wrap=False, scroll=None)

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
                        "Todas las publicaciones",
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
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        padding=ft.padding.only(left=0, right=0, top=12, bottom=0)
    )

    main_content = ft.Row(
        [
            ft.Container(
                content=ft.Column([filtros,
                                   ft.Text(f"Total publicaciones: {VISIBLE_CARDS}/{len(publicaciones_demo)}", size=14,
                                           color=TEXT_COLOR)]),
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

    page.add(header, tabs, main_content,confirm_dialog)


if __name__ == "__main__":
    ft.app(target=main)
