import flet as ft
from flet import Icons, Colors

def main(page: ft.Page):
    # Configuración general
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Cali Trabaja!"
    PRIMARY_COLOR = "#3EAEB1"
    BACKGROUND_COLOR = "#FAFAFA"
    page.window_width = 700
    page.window_height = 600
    page.window_resizable = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F7F7F7"

    # Header
    header = ft.Container(
        bgcolor="#F8F8F8",
        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            spacing=1,
            controls=[
                ft.Row(
                    spacing=1,
                    controls=[
                        ft.Image(src="../img/logo.jpg", width=82, height=82),
                        ft.Text("Cali", color=PRIMARY_COLOR, size=40, font_family="Oswald"),
                        ft.Text("Trabaja", color="#000000", size=40, font_family="Oswald"),
                    ],
                ),
                ft.Container(expand=True, alignment=ft.alignment.center_right),
            ],
        ),
    )

    # Función para crear campos
    def crear_campo(icono, etiqueta, password=False):
        return ft.Container(
            padding=ft.Padding(5, 3, 5, 3),  # Margen interno más compacto
            bgcolor="#e0e0e0",
            border_radius=15,
            content=ft.Row(
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(name=icono, color=PRIMARY_COLOR, size=18),
                    ft.TextField(
                        hint_text=etiqueta,
                        hint_style=ft.TextStyle(
                            font_family="Oswald",
                            weight=ft.FontWeight.BOLD,
                            size=13,
                            color=ft.Colors.BLACK54,
                        ),
                        text_style=ft.TextStyle(
                            font_family="Oswald",
                            size=13,
                            color=ft.Colors.BLACK
                        ),
                        border="none",
                        bgcolor="#e0e0e0",
                        password=password,
                        can_reveal_password=password,
                        text_align=ft.TextAlign.LEFT,
                        content_padding=ft.Padding(4, 4, 4, 4),  # Campo más delgado
                        height=36,
                        expand=True
                    )
                ]
            )
        )

    # Campos
    correo = crear_campo(Icons.ALTERNATE_EMAIL, "Correo electrónico")
    contrasena = crear_campo(Icons.LOCK_OUTLINE, "Contraseña", password=True)

    # Botón
    btn_iniciar_sesion = ft.ElevatedButton(
        text="Iniciar sesión",
        expand=True,
        height=40,
        width=150,
        style=ft.ButtonStyle(
            color={"": "black"},
            bgcolor={"": "#e0e0e0"},
            shape=ft.RoundedRectangleBorder(radius=6),
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Oswald"),
        )
    )

    # Contenedor del formulario
    contenedor = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Iniciar sesión", size=26, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR,
                        text_align=ft.TextAlign.CENTER),
                correo,
                contrasena,
                ft.Container(
                    content=btn_iniciar_sesion,
                    alignment=ft.alignment.center,
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=80,
        bgcolor="#FFFFFF",
        border_radius=25,
        width=450,
        height=330,
        alignment=ft.alignment.center_left,
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0"))
    )

    # Contenedor centrado con separación respecto al header
    body = ft.Container(
        content=contenedor,
        alignment=ft.alignment.center,
        expand=True,
        margin=ft.margin.only(top=60)  # Separación del header
    )

    # Agrega todo a la página
    page.add(
        ft.Column(
            controls=[header, body],
            expand=True
        )
    )

# Lanzar la app
if __name__ == "__main__":
    ft.app(target=main)
