import flet as ft

COLOR_TURQUESA = "#4ec3c7"
COLOR_BORDE = "#cfcfcf"


def main(page: ft.Page):
    page.title = "Perfil Experto - CaliTrabaja"
    page.bgcolor = "white"
    page.scroll = "adaptive"

    # HEADER
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(name="menu", size=28, color="black"),
                ft.Row([
                    ft.Image(src="https://i.imgur.com/MZgG2t5.png", width=35, height=35),  # Logo ficticio
                    ft.Text("Cali", size=20, weight="bold", color=COLOR_TURQUESA),
                    ft.Text("Trabaja", size=20, weight="bold", color="black"),
                ], spacing=5),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text("Cerrar Sesion", color="white", weight="bold"),
                    bgcolor=COLOR_TURQUESA,
                    border_radius=20,
                    padding=ft.padding.symmetric(horizontal=20, vertical=10)
                )
            ],
            alignment="spaceBetween",
            vertical_alignment="center",
        ),
        padding=ft.padding.all(10),
        border=ft.border.only(bottom=ft.BorderSide(1, "#e0e0e0")),
    )

    # TÍTULO
    title = ft.Container(
        content=ft.Text("Perfil Experto", size=24, weight="bold", color=COLOR_TURQUESA),
        alignment=ft.alignment.center,
        padding=ft.padding.symmetric(vertical=15)
    )

    # PERFIL IZQUIERDA
    profile_image = ft.Container(
        content=ft.Icon(name="person", size=60, color=COLOR_TURQUESA),
        border=ft.border.all(1, COLOR_BORDE),
        border_radius=100,
        padding=20
    )
    stars = ft.Row(
        [ft.Icon(name="star", color=COLOR_TURQUESA, size=20) for _ in range(5)],
        alignment="center"
    )

    left_column = ft.Column(
        [
            ft.Text("Angie Calderon", size=18, weight="bold"),
            profile_image,
            stars
        ],
        horizontal_alignment="center",
        spacing=10
    )

    # DESCRIPCIÓN Y EXPERIENCIA
    description = ft.Text(
        "Apasionada por el fitness, te ayudo a alcanzar tus metas de salud y fuerza "
        "con planes de entrenamiento personalizados. Mi enfoque combina disciplina "
        "y motivación para que logres tu mejor versión.",
        size=13
    )

    experience = ft.Column([
        ft.Text("Experiencia", size=14, weight="bold"),
        ft.Text("Coaching"),
        ft.Text("Smart Fit"),
        ft.Text("enero 2023 - septiembre 2024", size=12)
    ], spacing=3)

    studies = ft.Column([
        ft.Text("Mis estudios", size=14, weight="bold"),
        ft.Text("Técnico en actividad física"),
        ft.Text("Servicio nacional de aprendizaje"),
        ft.Text("julio 2022 - diciembre 2022", size=12)
    ], spacing=3)

    center_column = ft.Column(
        [
            ft.Text("Descripción:", size=14, weight="bold"),
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
                [ft.Text(titulo, size=14, weight="bold")] +
                [ft.Row([ft.Icon(name="check", color=COLOR_TURQUESA, size=18), ft.Text(txt)]) for txt in items],
                spacing=5
            ),
            border=ft.border.all(1, COLOR_BORDE),
            border_radius=10,
            padding=15
        )

    idiomas = cuadro_titulo("Idiomas", ["Español", "Inglés"])
    aptitudes = cuadro_titulo("Aptitudes", ["Liderazgo", "Comunicación efectiva"])

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


ft.app(target=main)