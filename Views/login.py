import flet as ft


def main(page: ft.Page):
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "Cali Trabaja!"
    page.window_width = 700
    page.window_height = 600
    page.window_resizable = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FAFAFA"

    # --- Header con logo personalizado ---
    header = ft.Container(
        bgcolor="#FFFFFF",
        padding=ft.padding.only(left=30, right=30, top=15, bottom=15),
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            spacing=10,
            controls=[
                ft.Image(src="../img/logo.png", width=32, height=32),
                ft.Text("Cali", color="#2FBDB3", size=20, font_family="Oswald"),
                ft.Text("Trabaja", color="#000000", size=20, font_family="Oswald"),
            ],
        ),
    )

    # --- Campos de login ---
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
                        text_size=14,
                        text_style=ft.TextStyle(font_family="Oswald")
                    )
                ],
                spacing=10
            ),
            bgcolor="#e0e0e0",
            border_radius=8,
            padding=10
        )

    correo = crear_campo(ft.Icons.ALTERNATE_EMAIL, "Correo electrónico")
    contrasena = crear_campo(ft.Icons.LOCK_OUTLINE, "Contraseña", password=True)

    btn_iniciar_sesion = ft.ElevatedButton(
        text="Iniciar sesión",
        expand=True,
        height=45,
        style=ft.ButtonStyle(
            color={"": "black"},
            bgcolor={"": "#FFFFFF"},
            shape=ft.RoundedRectangleBorder(radius=8),
            text_style=ft.TextStyle(weight=ft.FontWeight.BOLD, font_family="Oswald"),
        )
    )

    contenedor = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Iniciar sesión", size=24, weight=ft.FontWeight.BOLD, color="#3EAEB1",
                        text_align=ft.TextAlign.CENTER, font_family="Oswald"),
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
        bgcolor="#FFFFFF",
        border_radius=20,
        width=400,
        height=350,
        shadow=ft.BoxShadow(
            blur_radius=10,
            color="#E0E0E0",
            spread_radius=1,
            offset=ft.Offset(0, 5)
        ),
        alignment=ft.alignment.center,
    )

    # --- Centrado vertical ajustado ---
    main_col = ft.Column(
        controls=[
            ft.Container(height=page.window_height * 0.15),
            ft.Row(
                controls=[contenedor],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        expand=True
    )

    page.add(header, main_col)


if __name__ == "__main__":
    ft.app(target=main)
