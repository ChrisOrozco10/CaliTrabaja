import flet as ft
from flet import Icons
import inicio
from CaliTrabaja.API_services.iniciar_admin import iniciar_sesion_api

def main(page: ft.Page):
    # Configuración general
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Cali Trabaja!"
    PRIMARY_COLOR = "#3EAEB1"
    TEXT_COLOR = "#333333"
    page.window_resizable = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F7F7F7"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Header
    header = ft.Container(
        bgcolor="#F8F8F8",
        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=1,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(src="../img/logo.jpg", width=80, height=80),
                        ft.Text("Cali", color=PRIMARY_COLOR, size=40, font_family="Oswald"),
                        ft.Text("Trabaja", color="#000000", size=40, font_family="Oswald"),
                    ],
                ),
            ],
        ),
    )
     # Referencias directas
    correo_field = ft.TextField(
        hint_text="Correo electrónico",
        hint_style=ft.TextStyle(
            font_family="Oswald",
            weight=ft.FontWeight.BOLD,
            size=18,
            color=ft.Colors.BLACK54,
        ),
        text_style=ft.TextStyle(
            font_family="Oswald",
            size=18,
            color=ft.Colors.BLACK
        ),
        border_color="transparent",
        bgcolor="#e0e0e0",
        text_align=ft.TextAlign.LEFT,
        content_padding=ft.Padding(4, 4, 4, 4),
        height=36,
        expand=True
    )

    contrasena_field = ft.TextField(
        hint_text="Contraseña",
        hint_style=ft.TextStyle(
            font_family="Oswald",
            weight=ft.FontWeight.BOLD,
            size=18,
            color=ft.Colors.BLACK54,
        ),
        text_style=ft.TextStyle(
            font_family="Oswald",
            size=18,
            color=ft.Colors.BLACK
        ),
        border_color="transparent",
        bgcolor="#e0e0e0",
        password=True,
        can_reveal_password=True,
        text_align=ft.TextAlign.LEFT,
        content_padding=ft.Padding(4, 4, 4, 4),
        height=36,
        expand=True
    )

    # Función para envolver con icono
    def crear_campo(icono, campo):
        return ft.Container(
            padding=ft.Padding(5, 3, 5, 3),
            bgcolor="#e0e0e0",
            border_radius=15,
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(name=icono, color=PRIMARY_COLOR, size=18),
                    campo
                ]
            )
        )

    # Campos de login
    correo = crear_campo(Icons.ALTERNATE_EMAIL, correo_field)
    contrasena = crear_campo(Icons.LOCK_OUTLINE, contrasena_field)

    # Texto de error en la interfaz
    error_text = ft.Text(
        value="",
        color="red",
        size=18,
        visible=False
    )

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

    def cerrar_dialogo(e):
        page.dialog.open = False
        page.update()



    def abrir_usuarios(e):
        correo = correo_field.value
        contrasena = contrasena_field.value

        resultado = iniciar_sesion_api(correo, contrasena)

        if not resultado.get("success"):
            mensaje_error = resultado.get("message", "Error desconocido.")
            mostrar_snackbar(mensaje_error, exito=False)
        else:
            # Guardar token en la sesión
            page.session_token = resultado.get("token")

            mostrar_snackbar("Inicio de sesión exitoso.", exito=True)

            # Cargar vista principal
            page.clean()
            inicio.main(page)

    # Contenedor Login (Responsive)
    def crear_contenedor_login(width):
        responsive_width = 450 if width > 600 else width * 0.9
        padding_value = 80 if width > 600 else 20

        return ft.Container(
            padding=padding_value,
            bgcolor="#FFFFFF",
            border=ft.border.all(1, TEXT_COLOR),
            border_radius=25,
            width=responsive_width,
            content=ft.Column(
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text("Iniciar sesión", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR,
                            text_align=ft.TextAlign.CENTER),
                    correo,
                    contrasena,
                    ft.ElevatedButton(
                        text="Iniciar sesión",
                        expand=True,
                        height=45,
                        on_click=abrir_usuarios,
                        style=ft.ButtonStyle(
                            color="black",
                            bgcolor="#e0e0e0",
                            shape=ft.RoundedRectangleBorder(radius=6),
                            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Oswald", size=18),
                        ),
                    ),
                    error_text
                ]
            )
        )

    # Función de construcción responsive
    def construir_pagina(e=None):
        page.controls.clear()
        contenedor_login = crear_contenedor_login(page.width)

        body = ft.Container(
            content=contenedor_login,
            alignment=ft.alignment.center,
            expand=True,
            margin=ft.margin.only(top=95),
        )

        page.add(
            ft.Column(
                expand=True,
                controls=[
                    header,
                    body
                ]
            )
        )

        page.update()

    page.on_resize = construir_pagina
    construir_pagina()

# Ejecutar app en navegador
if __name__ == "__main__":
    ft.app(target=main)
