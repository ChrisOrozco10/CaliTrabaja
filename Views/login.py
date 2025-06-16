import flet as ft


def main(page: ft.Page):
    # Configuración general
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Cali Trabaja!"
    page.window_width = 700
    page.window_height = 600
    page.window_resizable = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#D9D9D9"

    def crear_campo(icono, etiqueta, password=False):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(name=icono, color="#3EAEB1", size=20),
                    ft.TextField(
                        label=ft.Text(etiqueta, weight=ft.FontWeight.BOLD),
                        border="none",
                        bgcolor="#e0e0e0",
                        password=password,
                        can_reveal_password=password,
                        expand=True,
                        height=45,
                        text_size=14
                    )
                ],
                spacing=10
            ),
            bgcolor="#e0e0e0",
            border_radius=8,
            padding=10
        )

        # Reemplazamos la imagen del logo por un texto

    logo_text = ft.Text(
        "Cali Trabaja!",
        size=32,
        weight=ft.FontWeight.BOLD,
        color="#3EAEB1",
        text_align=ft.TextAlign.CENTER
    )

    correo = crear_campo(ft.Icons.ALTERNATE_EMAIL, "Correo electrónico")
    contrasena = crear_campo(ft.Icons.LOCK_OUTLINE, "Contraseña", password=True)

    btn_iniciar_sesion = ft.ElevatedButton(
        text="Iniciar sesión",
        expand=True,
        height=45,
        style=ft.ButtonStyle(
            color={"": "white"},
            bgcolor={"": "#3EAEB1"},
            shape=ft.RoundedRectangleBorder(radius=8),
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Oswald"),
        )
    )

    contenedor = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=logo_text, alignment=ft.alignment.center, padding=ft.padding.only(bottom=20)),
                ft.Text("Iniciar sesión", size=28, weight=ft.FontWeight.BOLD, color="#3EAEB1",
                        text_align=ft.TextAlign.CENTER),
                correo,
                contrasena,
                ft.Container(content=btn_iniciar_sesion, alignment=ft.alignment.center,
                             padding=ft.padding.only(top=20))
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        ),
        padding=30,
        bgcolor="#66FFFFFF",
        border_radius=20,
        width=450,
        height=400
    )

    # Contenedor principal centrado
    main_container = ft.Container(
        content=contenedor,
        alignment=ft.alignment.center,
        expand=True
    )

    # Fila principal centrada
    main_row = ft.Row(
        controls=[main_container],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    page.add(main_row)


if __name__ == "__main__":
    ft.app(target=main)