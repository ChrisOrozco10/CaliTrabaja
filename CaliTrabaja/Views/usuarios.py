import flet as ft
import reportes
import crearADMIN
import publicaciones
import login
import inicio
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.obtener_usuarios import gestionar_usuarios_admin
from CaliTrabaja.API_services.iniciar_admin import iniciar_sesion_api

def main(page: ft.Page):

    correo="jupahure@gmail.com"
    contrasena="A1234567"

    resultado = iniciar_sesion_api(correo, contrasena)
    if not resultado or not resultado.get("success"):
        page.add(ft.Text("No se pudo iniciar sesión"))
    else:
        token = resultado.get("token")
        setattr(page, "session_token", token)


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

    # -------------------- Modal de Confirmación ---------------------------
    dialog_title = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    dialog_description = ft.Text("", size=16)
    dialog_textfield = ft.TextField(hint_text="Descripción...", border_radius=10, multiline=True, height=80)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=dialog_title,
        content=ft.Container(
            height=110,
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
                        on_click= cerrar_sesion
                    )
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
                            options=[ft.dropdown.Option(o) for o in ["Todos", "Experto", "Cliente", "Admin"]],
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
                            options=[ft.dropdown.Option(o) for o in ["Todos", "Activo", "Deshabilitado"]],
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
                            options=[ft.dropdown.Option(o) for o in ["Todas", "1", "2"]],
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



    def tarjeta_usuario(nombre, rol, categoria, estado, fecha, correo, id_user, publicaciones, reportes, rating):


        controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(nombre, size=20, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.PopupMenuButton(
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
                                on_click=lambda e: abrir_confirmacion(nombre, "notificar un problema", id_user)
                            ),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.BLOCK, color="#333333", size=20),
                                        ft.Text("Deshabilitar Cuenta", color="#333333"),
                                    ],
                                    spacing=10,
                                ),
                                on_click=lambda e: abrir_confirmacion(nombre, "deshabilitar la cuenta", id_user)
                            ),
                        ],
                    )
                ]
            ),
            ft.Text(f"Rol: {rol}", size=18, color="#333333"),
            ft.Text(f"Estado: {estado}", size=18, color="#333333"),
            ft.Text(f"Se unió el {fecha}", size=18, color="#333333"),
            ft.Text(f"Correo: {correo}", size=18, color="#333333"),
            ft.Text(f"ID: {id_user}", size=18, color="#333333"),
        ]

        if rol:
            controls.insert(1, ft.Row([
                ft.Icon(ft.Icons.STAR if i < rating else ft.Icons.STAR_BORDER, color="#2FBDB3", size=24)
                for i in range(5)
            ]))
            controls.insert(2, ft.Text(f"Categoría: {categoria}", size=18, color="#333333"))
            controls.append(
                ft.Row(
                    spacing=15,
                    controls=[
                        ft.ElevatedButton(
                            f"Publicaciones {publicaciones}",
                            bgcolor="#F5F5F5",
                            color="#333333",
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(width=2, color="#2FBDB3"),
                                shape=ft.RoundedRectangleBorder(radius=20),
                            ),
                        ),
                        ft.ElevatedButton(
                            f"Reportes {reportes}",
                            bgcolor="#F5F5F5",
                            color="#333333",
                            style=ft.ButtonStyle(
                                side=ft.BorderSide(width=2, color="#D9D9D9"),
                                shape=ft.RoundedRectangleBorder(radius=20),
                            ),
                        ),
                    ],
                )
            )

        return ft.Container(
            bgcolor="#FFFFFF",
            padding=30,
            content=ft.Column(
                spacing=10,
                controls=controls
            ),
            border_radius=10,
            border=ft.border.all(1, "#DDDDDD"),
            height=400,
            width=400,
        )

    def obtener_usuario(page):
        # Obtener el token de la sesión


        token = getattr(page, "session_token", None)
        if not token:
            page.add(ft.Text("Debe iniciar sesión primero"))
            return

        # Traer los usuarios desde la API
        usuarios = gestionar_usuarios_admin(token)
        print("Usuarios recibidos de la API:", usuarios)
        if not usuarios:
            return [ft.Text("No se pudo obtener usuarios")]

        tarjetas = []



        for usuario in usuarios:
            # Si usuario es un diccionario, usamos .get(), si no, asumimos que es un string
            if isinstance(usuario, dict):
                nombre = f"{usuario.get('primer_nombre', '')} {usuario.get('primer_apellido', '')}"
                rol = usuario.get("tipo_rol", "N/A")

                # Formatear lista de categorías
                categorias_lista = usuario.get("categorias", [])

                if isinstance(categorias_lista, list):
                    categoria = ", ".join(categorias_lista) if categorias_lista else "N/A"
                else:
                    categoria = categorias_lista or "N/A"

                estado = usuario.get("estado", "N/A")
                registro = usuario.get("fecha_registro", "N/A")
                correo = usuario.get("correo", "N/A")
                id_user = usuario.get("usuario_id", "N/A")
                publicaciones = usuario.get("publicaciones", 0)
                reportes = usuario.get("reportes", 0)
                rating = usuario.get("rating", 0)


            tarjetas.append(
                tarjeta_usuario(
                    nombre=nombre,
                    rol = rol,
                    categoria = categoria,
                    estado = estado,
                    fecha= registro,
                    correo = correo,
                    id_user= id_user,
                    publicaciones=publicaciones,
                    reportes=reportes,
                    rating=rating
                )
            )
        return tarjetas




    # -------------------- Carrusel -----------------------------------------
    CARD_WIDTH     = 400
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
    tarjetas = obtener_usuario(page)  # Defínelo primero

    def actualizar_tarjetas():
        nonlocal tarjetas
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
        padding=ft.padding.only(left=5),
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

        ],

    )

    total_usuarios = len(tarjetas)
    filtros_y_total = ft.Column([
        filtros,
        ft.Container(
            content=ft.Text(f"Total de usuarios: {total_usuarios}", size=14, color=TEXT_COLOR),
            padding=ft.padding.only(top=20),
            alignment=ft.alignment.center,
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    main_content = ft.ResponsiveRow([
        ft.Container(content=filtros_y_total, col={'sm': 12, 'md': 4, 'lg': 3}),
        ft.Container(content=reportes_container, col={'sm': 12, 'md': 8, 'lg': 9}),
    ], spacing=20)

    page.add(header, tabs, main_content,confirm_dialog)


if __name__ == "__main__":
    ft.app(target=main)
