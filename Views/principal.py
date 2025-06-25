import flet as ft
import login
def main(page: ft.Page):
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    page.title = "CaliTrabaja! - Bienvenida"
    page.bgcolor = "#F7F7F7"
    page.window_width = 700
    page.window_height = 600
    page.window_resizable = False

    def abrir_login(e):
        page.clean()
        login.main(page)

    # Logo o encabezado visual
    logo_text = ft.Text(
        "CaliTrabaja!",
        size=36,
        weight=ft.FontWeight.BOLD,
        color="#3EAEB1"
    )

    subtitle = ft.Text(
        "Bienvenido al área administrativa de CaliTrabaja!",
        size=18,
        color="#555555"
    )

    # Botón que lanza login.main
    btn_iniciar = ft.ElevatedButton(
        text="Iniciar sesión",
        bgcolor="#3EAEB1",
        color="white",
        height=45,
        width=180,
        on_click=abrir_login,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=22, font_family="Oswald"),
        )
    )

    footer = ft.Text(
        "¡Comienza hoy mismo a encontrar o publicar servicios fácilmente!",
        size=14,
        color="#888888",
        italic=True
    )

    container = ft.Container(
        content=ft.Column(
            [
                logo_text,
                subtitle,
                ft.Divider(height=20, color="transparent"),
                btn_iniciar,
                ft.Divider(height=30, color="transparent"),
                footer
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        bgcolor="#66FFFFFF",
        border_radius=25,
        padding=40,
        width=450,
        height=350
    )

    page.add(
        ft.Row(
            controls=[container],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)