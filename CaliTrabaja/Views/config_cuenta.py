import flet as ft
import inicio
import login
import crearADMIN
import config_Des
import config_Contra
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.datos_admin import obtener_datos_admin

def main(page: ft.Page):

    def obtener_token(page):
        return getattr(page, "session_token", None)
    # ---------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    CARD_BACKGROUND = "#FFFFFF"
    page.bgcolor = "white"
    page.padding = 0
    page.spacing = 0
    page.window_width = 1920
    page.window_height = 1080

    # ---------------------- FUNCIONES AUXILIARES ----------------------
    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        if isinstance(e.control.title, ft.Text):
            title = e.control.title.value
            if title == "Inicio":
                inicio.main(page)
            if title == "Crear Usuario Administrador":
                crearADMIN.main(page)
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

        # ---------------------------------------------------------------

    # ---------------------- DRAWER ----------------------
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
                            title=ft.Text("Inicio", size=18, color=TEXT_COLOR, font_family="Oswald"),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Configuración de cuenta", size=18, color=TEXT_COLOR, font_family="Oswald"),
                            on_click=on_drawer_item_click,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON_ADD_OUTLINED, size=28, color=TEXT_COLOR),
                            title=ft.Text("Crear Usuario Administrador", size=18, color=TEXT_COLOR, font_family="Oswald"),
                            on_click=on_drawer_item_click,
                        ),
                    ],
                ),
            )
        ],
    )

    # ---------------------- HEADER ----------------------
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

    # ---------------------- CONTENIDO PRINCIPAL ----------------------


    def obtener_datos():
        token = obtener_token(page)

        if not token:
            page.add(ft.Text("Debes iniciar sesion primero"))
            return None

        respuesta = obtener_datos_admin(token)

        if respuesta.get("success") == True:
            datos = respuesta.get("datos")

            nombre_usuario = f"{datos['primer_nombre']} {datos['primer_apellido']}"
            fecha_union = datos["fecha_registro"]  # 👈 viene de la BD
            rol_usuario = datos["rol"]  # 👈 viene de la BD





            tarjeta_info = ft.Container(
            padding=15,
            width=700,
            bgcolor=CARD_BACKGROUND,
            border=ft.border.all(1, "#CCCCCC"),
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Text(f"Nombre de usuario:{nombre_usuario}", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, font_family="Oswald"),
                    ft.Text(f"Se unio el: {fecha_union}", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, font_family="Oswald"),
                    ft.Text(f"Rol actual: {rol_usuario}", size=20, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, font_family="Oswald"),
                ]
            )
        )
        return tarjeta_info








    tarjeta_cambiar_contra = ft.Container(
        padding=15,
        width=700,
        bgcolor=CARD_BACKGROUND,
        border=ft.border.all(1, "#CCCCCC"),
        border_radius=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("¿Necesitas cambiar tu contraseña? Hazlo en segundos.", size=20,color=TEXT_COLOR, font_family="Oswald"),
                ft.ElevatedButton(
                    "Cambiar contraseña",
                    bgcolor="#F5F5F5",
                    color="black",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        side=ft.BorderSide(width=2, color="#2FBDB3",),
                        text_style=ft.TextStyle(font_family="Oswald", size=20),
                    ),
                    on_click=lambda e: (page.clean(), config_Contra.main(page))
                )
            ]
        )
    )

    tarjeta_eliminar_cuenta = ft.Container(
        padding=15,
        width=700,
        bgcolor=CARD_BACKGROUND,
        border=ft.border.all(1, "#CCCCCC"),
        border_radius=10,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Esta opción hace que tu cuenta se elimine de manera definitiva.", size=20, color=TEXT_COLOR, font_family="Oswald"),
                ft.ElevatedButton(
                    "Eliminar cuenta",
                    bgcolor="#F5F5F5",
                    color="black",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                        side=ft.BorderSide(width=2, color="#2FBDB3"),
                        text_style=ft.TextStyle(font_family="Oswald", size=20),
                    ),
                    on_click=lambda e: (page.clean(), config_Des.main(page))
                )
            ]
        )
    )
    tarjeta_info = obtener_datos()

    contenido = ft.Container(
        margin=ft.margin.only(top=100),
        content=ft.Column(
            controls=[
                ft.Row([tarjeta_info], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([tarjeta_cambiar_contra], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([tarjeta_eliminar_cuenta], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
        )
    )

    # ---------------------- AGREGAR A LA PÁGINA ----------------------
    page.add(header, contenido)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
