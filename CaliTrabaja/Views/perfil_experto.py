import flet as ft
import crearADMIN
import inicio
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
import login
from CaliTrabaja.API_services.datos_expertos import  obtener_datos_expertos

def main(page: ft.Page):
    # Configuración general
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Perfil Experto - CaliTrabaja"
    page.bgcolor = "white"
    page.scroll = "adaptive"

    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    COLOR_BORDE = "#cfcfcf"

    # -------------------- Drawer ------------------------------------------
    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def obtener_token(page):
        return getattr(page, "session_token", None)

    def obtener_id(page):
        return getattr(page, "usuario_id", None)

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

    def procesar_datos_expertos(page):

        token = obtener_token(page)
        id_usuario = obtener_id(page)
        if not token:
            print("Necesita tener el token.")


        informacion = {}

        if id_usuario:
            informacion["usuario_id"] = id_usuario

        respuesta = obtener_datos_expertos(token, informacion)

        print(f"ID:{informacion}, Token:{token} ")

        print("Datos de experto", respuesta)

        datos = respuesta.get("expertos", {})

        # Extraer valores con defaults
        primer_nombre = datos.get("primer_nombre", "N/A")
        primer_apellido = datos.get("primer_apellido", "N/A")
        descripcion = datos.get("descripcion") or "N/A"
        nombre_experiencia = datos.get("nombre_experiencia") or "N/A"
        descripcion_experiencia = datos.get("descripcion_experiencia") or "N/A"
        fecha_inicio_experiencia = datos.get("fecha_inicio_experiencia") or "N/A"
        fecha_fin_experiencia = datos.get("fecha_fin_experiencia") or "N/A"
        titulo_obtenido = datos.get("titulo_obtenido") or "N/A"
        institucion = datos.get("institucion") or "N/A"
        fecha_inicio_estudios = datos.get("fecha_inicio_estudios") or "N/A"
        fecha_fin_estudios = datos.get("fecha_fin_estudios") or "N/A"
        tipo_aptitud = datos.get("tipo_aptitud")

        # Asegurar que idiomas_items sea una lista
        idiomas_items = [i.get("nombre_idioma") for i in (datos.get("idiomas") or [])]

        # Asegurar que aptitudes_items sea lista
        aptitudes_items = [tipo_aptitud] if tipo_aptitud else []

        return {
            "nombre_usuario": f"{primer_nombre} {primer_apellido}",
            "descripcion": descripcion,
            "nombre_experiencia": nombre_experiencia,
            "descripcion_experiencia": descripcion_experiencia,
            "fecha_inicio_experiencia": fecha_inicio_experiencia,
            "fecha_fin_experiencia": fecha_fin_experiencia,
            "titulo_obtenido": titulo_obtenido,
            "institucion": institucion,
            "fecha_inicio_estudios": fecha_inicio_estudios,
            "fecha_fin_estudios": fecha_fin_estudios,
            "tipo_aptitud": tipo_aptitud,
            "idiomas_items": idiomas_items,
            "aptitudes_items": aptitudes_items
        }


    datos_expertos = procesar_datos_expertos(page)

    if datos_expertos:
        nombre_usuario = datos_expertos.get("nombre_usuario")
        descripcion = datos_expertos.get("descripcion")
        nombre_experiencia = datos_expertos.get("nombre_experiencia")
        descripcion_experiencia = datos_expertos.get("descripcion_experiencia")
        fecha_inicio_experiencia = datos_expertos.get("fecha_inicio_experiencia")
        fecha_fin_experiencia = datos_expertos.get("fecha_fin_experiencia")
        titulo_obtenido = datos_expertos.get("titulo_obtenido")
        institucion = datos_expertos.get("institucion")
        fecha_inicio_estudios = datos_expertos.get("fecha_inicio_estudios")
        fecha_fin_estudios = datos_expertos.get("fecha_fin_estudios")
        idiomas_items = datos_expertos.get("idiomas_items")
        aptitudes_items = datos_expertos.get("aptitudes_items")

    # TÍTULO
    title = ft.Container(
        content=ft.Text("Perfil Experto", size=26, weight="bold", color=PRIMARY_COLOR),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=15)
    )

    # PERFIL IZQUIERDA
    profile_image = ft.Container(
    content=ft.Icon(name="person", size=60, color=PRIMARY_COLOR),
    border=ft.border.all(1, COLOR_BORDE),
            border_radius=100,
            padding=20
        )
    stars = ft.Row(
            [ft.Icon(name="star", color=PRIMARY_COLOR, size=20) for _ in range(5)],
            alignment="center"
        )

    left_column = ft.Column(
        [
            ft.Text(nombre_usuario, size=18, weight="bold", color=TEXT_COLOR),
            profile_image,
            stars
        ],
        horizontal_alignment="center",
        spacing=10
    )

    # DESCRIPCIÓN Y EXPERIENCIA
    description = ft.Text(
        descripcion,
        size=13, color=TEXT_COLOR
    )

    experience = ft.Column([
        ft.Text("Experiencia", size=14,color=TEXT_COLOR, weight="bold"),
        ft.Text(nombre_experiencia, color=TEXT_COLOR),
        ft.Text(descripcion_experiencia, color=TEXT_COLOR),
        ft.Text(f"{fecha_inicio_experiencia}- {fecha_fin_experiencia}", size=12, color=TEXT_COLOR),
    ], spacing=3)

    studies = ft.Column([
        ft.Text("Mis estudios", size=14, weight="bold", color=TEXT_COLOR),
        ft.Text(titulo_obtenido, color=TEXT_COLOR),
        ft.Text(institucion, color=TEXT_COLOR ),
        ft.Text(f"{fecha_inicio_estudios} - {fecha_fin_estudios}", size=12, color=TEXT_COLOR)
    ], spacing=3)

    center_column = ft.Column(
        [
            ft.Text("Descripción:", size=14, weight="bold", color=TEXT_COLOR),
            description,
            ft.ResponsiveRow([
                ft.Column([experience], col={"xs": 12, "sm": 6}),
                ft.Column([studies], col={"xs": 12, "sm": 6}),
            ])
        ],
        spacing=12
        )

    # CUADRO DE IDIOMAS Y APTITUDES
    def cuadro_titulo(titulo, items):
        return ft.Container(
            content=ft.Column(
                [ft.Text(titulo, size=14, weight="bold", color=TEXT_COLOR)] +
                [ft.Row([ft.Icon(name="check", color=PRIMARY_COLOR, size=18), ft.Text(txt, color=TEXT_COLOR)]) for txt in items],
                spacing=5
            ),
            border=ft.border.all(1, COLOR_BORDE),
            border_radius=10,
            padding=15
        )

    idiomas = cuadro_titulo("Idiomas", idiomas_items)
    aptitudes = cuadro_titulo("Aptitudes",aptitudes_items)

    right_column = ft.Column([idiomas, aptitudes], spacing=15)

    # CARD PRINCIPAL
    main_card = ft.Container(
        content=ft.ResponsiveRow([
            ft.Column([left_column], col={"xs": 12, "sm": 3}),
            ft.Column([center_column], col={"xs": 12, "sm": 6}),
            ft.Column([right_column], col={"xs": 12, "sm": 3}),
        ], alignment="spaceBetween"),
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=10,
        padding=80
    )

    # PÁGINA
    page.add(
        header,
        title,
        ft.Container(content=main_card, padding=ft.padding.all(10))
    )


