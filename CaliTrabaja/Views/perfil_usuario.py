import flet as ft
from flet.core.border_radius import horizontal
import crearADMIN
import inicio
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.datos_clientes import obtener_datos_clientes
import login
import usuarios
import publicaciones
import reportes

def main(page: ft.Page):
    """
    Interfaz responsive del perfil de usuario con sección de calificaciones.
    """
    # Configuración general
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Perfil Usuario - CaliTrabaja"
    page.bgcolor = "#FFFFFF"
    page.scroll = "adaptive"

    # Colores
    accent_color = "#26B2B8"
    star_color = "#26B2B8"
    text_black = "#000000"
    text_gray = "#666666"

    PRIMARY_COLOR    = "#2FBDB3"     # ← Color turquesa (flechas y otros elementos)
    BORDER_COLOR     = "#DDDDDD"
    TEXT_COLOR       = "#333333"

    # ============================
    # DATOS DE EJEMPLO DEL CARRUSEL
    # ============================
    calificaciones = [
        dict(nombre="Angela Martínez", rating=5,
             comentario="Excelente trabajador, cumplió con todas sus responsabilidades, muy puntual."),

        dict(nombre="Carlos Pérez", rating=3,
             comentario="Buen trabajo en general, aunque tardó un poco más de lo esperado."),

        dict(nombre="María García", rating=4, comentario="Muy responsable y dedicada en su labor."),

        dict(nombre="Juan Rodríguez", rating=2, comentario="Debe mejorar en puntualidad."),
    ]

    # -------------------- Drawer ------------------------------------------

    def obtener_token(page):
        return getattr(page, "session_token", None)

    def obtener_id(page):
        return getattr(page, "usuario_id", None)



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

    def mostrar_snackbar(mensaje, exito=True):
        """Muestra SnackBar con estilo uniforme"""
        sb = ft.SnackBar(
            content=ft.Text(mensaje),
            bgcolor=ft.Colors.GREEN if exito else ft.Colors.RED,
            duration=3000
        )
        page.overlay.append(sb)
        sb.open = True
        page.update()

    def cerrar_sesion(e):
        respuesta = cerrar_sesion_api()
        page.clean()
        login.main(page)

        if respuesta.get("success"):
            mostrar_snackbar("Sesión cerrada correctamente.", exito=True)
        else:
            mostrar_snackbar(respuesta.get("message", "Error al cerrar sesión"), exito=False)

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

    def procesar_datos_clientes(page):
        token = obtener_token(page)
        usuario_id = obtener_id(page)

        if not token:
            print("Debes iniciar sesion para entrar")

        informacion ={}

        if usuario_id:
            informacion["usuario_id"] = usuario_id

        respuesta = obtener_datos_clientes(token, informacion)

        print("Datos", respuesta)

        datos=respuesta.get("clientes", {})

        primer_nombre = datos.get("primer_nombre") or "N/A"
        primer_apellido = datos.get("primer_apellido") or "N/A"
        direccion = datos.get("direccion") or  "N/A"

        return {
            "nombre_usuario": f"{primer_nombre}  {primer_apellido}",
            "direccion": direccion
        }

    datos = procesar_datos_clientes(page)
    if datos:
        nombre= datos.get("nombre_usuario")
        direccion = datos.get("direccion")

    print(f"NOMBRE: {nombre}, DIRECCION: {direccion}")

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
    # -------------------- Pestañas ----------------------------------------
    tabs = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Row(
            controls=[
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
    # FUNCIÓN: ESTRELLAS
    def estrellas(rating: int):
        return ft.Row(
            [ft.Icon("star", color=star_color, size=14) for _ in range(rating)] +
            [ft.Icon("star_border", color=star_color, size=14) for _ in range(5 - rating)],
            alignment="start",
            spacing=1
        )

    # TARJETA DE CALIFICACIÓN
    def tarjeta_calificacion(c: dict):
        return ft.Container(
            width=250,   # ancho compacto
            height=200,
            padding=12,
            border=ft.border.all(1, "#333333"),
            border_radius=12,
            bgcolor="white",
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.CircleAvatar(bgcolor="#EAEAEA", radius=18),
                            ft.Column([
                                ft.Text(
                                    c["nombre"],
                                    weight="bold",
                                    size=14,
                                    color="#000000"
                                ),
                                estrellas(c["rating"]),
                            ], spacing=3)
                        ],
                        alignment="start",
                        vertical_alignment="center"

                    ),
                    ft.Text(
                        c["comentario"],
                        size=12,
                        color="#000000",
                        max_lines=3,
                        overflow="ellipsis"
                    )
                ],
                spacing=5
            )


            )

    # PERFIL (IZQUIERDA)
    perfil_col = ft.Container(
        width=380,
        padding=20,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(nombre, size=22, weight="bold", color=text_black),
                        ft.CircleAvatar(content=ft.Icon(name="person", size=60), radius=40, bgcolor="#26B2B8"),
                        ft.Row(
                            [ft.Icon(name="star", color=star_color, size=20) for _ in range(5)],
                            alignment="center"
                        )
                    ],
                    alignment="center",
                    spacing=10,
                    horizontal_alignment="center",
                ),
                ft.VerticalDivider(width=20, color="transparent"),
                ft.Column(
                    [
                        ft.Text("Ubicación", size=18, weight="bold", color=text_black),
                        ft.Text("Direccion", size=16, weight="normal", color=text_black),
                        ft.Text(direccion, size=14, color=text_gray),
                    ],
                    spacing=5,
                    alignment="start",
                    horizontal_alignment="start",
                )
            ],
            alignment="start",
            vertical_alignment="center"
        ),
    )

    # CALIFICACIONES (CARRUSEL)
    carrusel = ft.Row(
        [tarjeta_calificacion(c) for c in calificaciones],
        scroll="hidden",
        height=220,
        expand=True,
        alignment="start",
        spacing=20
    )

    def mover_carrusel(direccion: str):
        if direccion == "izq":
            carrusel.scroll_to(delta=-300, duration=400)
        elif direccion == "der":
            carrusel.scroll_to(delta=300, duration=400)

    calif_seccion = ft.Container(
        expand=True,
        padding=10,
        content=ft.Container(
            border=ft.border.all(1, "#333333"),
            border_radius=18,
            padding=20,
            bgcolor="#FFFFFF",
            content=ft.Column(
                [
                    ft.Text("Calificaciones", size=24, weight="bold", color=accent_color),
                    ft.Row(
                        [
                            ft.IconButton("chevron_left", on_click=lambda _: mover_carrusel("izq"), icon_color=accent_color),
                            ft.Container(content=carrusel, expand=True),
                            ft.IconButton("chevron_right", on_click=lambda _: mover_carrusel("der"), icon_color=accent_color),
                        ],
                        alignment="center",
                        vertical_alignment="center"
                    )
                ],
                spacing=10
            ),
        )
    )

    # TARJETA PRINCIPAL (PERFIL + CALIFICACIONES)
    card_principal = ft.Row(
        [
            perfil_col,
            ft.VerticalDivider(width=110, color="transparent"),
            calif_seccion,
        ],
        alignment="start",
        vertical_alignment="center",
    )

    # PÁGINA
    page.add(
        header,tabs,
        ft.Row(
            [
                ft.Text(
                    "Perfil Usuario",
                    size=26,
                    weight="bold",
                    color=accent_color
                )
            ],
            alignment="center"  # <-- centra el contenido

        ),
        ft.Container(height=30),

        ft.Container(
            border=ft.border.all(1, "#333333"),
            border_radius=12,
            padding=30,
            content=card_principal,
            expand=True,
        )
    )


