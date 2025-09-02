import flet as ft
import publicaciones
import crearADMIN
from flet import Icons, Colors
import datetime
import usuarios
import login
import inicio
import perfil_usuario
import perfil_experto
from CaliTrabaja.API_services.obtener_reportes import gestionar_reportes_admin
from CaliTrabaja.Views import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.iniciar_admin import iniciar_sesion_api


def main(page: ft.Page):
    global tarjetas_container, tarjetas

    def obtener_token(page):
        return  getattr(page, "session_token", None)


    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "#DDDDDD"
    TEXT_COLOR = "#333333"
    ARROW_SPACING = 30


    page.title = "CaliTrabaja - Reportes"
    page.window_maximized = True
    page.bgcolor = BACKGROUND_COLOR
    page.padding = 20

    selected_date_text = ft.Text("Sin seleccionar", size=12, color=Colors.BLACK45)

    def update_date_text(e):
        selected_date_text.value = f"Seleccionado: {e.control.value}"
        page.update()

    date_picker = ft.DatePicker(
        on_change=update_date_text,
        first_date=datetime.date(2020, 1, 1),
        last_date=datetime.date(2030, 12, 31),
    )
    page.overlay.append(date_picker)

    def open_date_picker():
        date_picker.open = True
        page.update()

    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def on_drawer_item_click(e):
        if isinstance(e.control.title, ft.Text):
            title = e.control.title.value
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
        # ---------------------------------------------------------------

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
                color= TEXT_COLOR,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(width=2, color="#D9D9D9"),
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                on_click=lambda e: cerrar_dialogo()
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Función para cerrar el diálogo
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

    tabs = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Row(
            [
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
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
                        padding=10,
                        text_style=ft.TextStyle(size=24, font_family="Oswald", weight=ft.FontWeight.BOLD),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30,
        ),
        # Configuracion
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=25,
        padding=5,
        # Re-cuadro
        margin=ft.margin.only(top=5, bottom=20, left=250, right=250),

    )

    #-----------------------Variable de los reportes ---------------------

    id_reporte_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)
    fecha_reporte_field = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH,  tooltip="Seleccionar fecha", on_click=lambda e: open_date_picker())
    id_usuario_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)
    rol_dropdown = ft.Dropdown(
        width=120,
        text_size=12,
        border_radius=5,
        value="Todos",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("experto"),
            ft.dropdown.Option("cliente"),
        ],
    )

    filtros = ft.Container(
        content=ft.Column(
            [
                ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=Colors.BLACK54),

                ft.Row(
                    [
                        ft.Text("ID Reporte", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                        id_reporte_field,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                ft.Row(
                    [
                        ft.Text("ID Usuario", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                        id_usuario_field,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                # --- Rol ---
                ft.Row(
                    controls=[
                        ft.Text("Rol", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                        rol_dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            spacing=8,
        ),
        padding=12,
        bgcolor=CARD_BACKGROUND,
        height=300,  # aumentado para que quepa el nuevo campo
        width=260,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    # Contenedor para las tarjetas (inicialmente vacío)
    tarjetas_container = ft.Row(
        controls=[],  # Inicia el Row vacío
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        wrap=False,  # Cambié a True para que las tarjetas puedan ocupar varias filas si es necesario
        expand=True
    )

    tarjetas_todas = []
    tarjetas_filtradas = []
    tarjetas_actuales = []  # <- Lista activa
    start_index = 0

    VISIBLE_CARDS = 2
    CARD_WIDTH = 380
    CARD_HEIGHT = 300
    CARD_SPACING = 20
    ARROW_SPACING = CARD_WIDTH + CARD_SPACING  # 300 px
    CAROUSEL_WIDTH = VISIBLE_CARDS * CARD_WIDTH + (VISIBLE_CARDS - 1) * CARD_SPACING

    tarjetas_container = ft.Row(
        spacing=10,
        expand=True,
        wrap=False,
        scroll=None,
    )

    def actualizar_tarjetas(page, start_index, tarjetas_lista):
        tarjetas_container.controls.clear()

        if not tarjetas_lista:
            # Mantener altura y ancho fijo para que el carrusel no se suba
            tarjetas_container.controls.append(
                ft.Container(
                    content=ft.Text("No hay reportes disponibles.", color="red"),
                    alignment=ft.alignment.center,
                    width=CAROUSEL_WIDTH,  # mismo ancho del carrusel
                    height=400,   # misma altura de las tarjetas
                    padding=ft.padding.only(left=-20),
                )

            )
            total_reportes = 0
        else:
            # Mostrar las visibles según el índice
            visibles = tarjetas_lista[start_index:start_index + VISIBLE_CARDS]
            tarjetas_container.controls.extend(visibles)
            total_reportes = len(tarjetas_lista)

        actualizar_total_reportes(total_reportes)
        page.update()

    def siguiente(e):
        global start_index, tarjetas_actuales
        if tarjetas_actuales:
            if start_index + VISIBLE_CARDS < len(tarjetas_actuales):
                start_index += VISIBLE_CARDS
            else:
                start_index = len(tarjetas_actuales) - (len(tarjetas_actuales) % VISIBLE_CARDS or VISIBLE_CARDS)
            actualizar_tarjetas(e.page, start_index, tarjetas_actuales)

    def anterior(e):
        global start_index, tarjetas_actuales
        if tarjetas_actuales:
            if start_index - VISIBLE_CARDS >= 0:
                start_index -= VISIBLE_CARDS
            else:
                start_index = 0
            actualizar_tarjetas(e.page, start_index, tarjetas_actuales)




    def obtener_reportes(page, reporte_id=None, reportador_id=None, rol=None ):
        # Obtener el token de la sesión

        token = obtener_token(page)


        if not token:
            page.add(ft.Text("Debe iniciar sesión primero"))
            return[]

        filtros = {}
        if reporte_id:
            filtros["reporte_id"] = reporte_id
        if reportador_id:
            filtros["reportador_id"] = reportador_id
        if rol and rol != "Todos":
            filtros["tipo_rol"] = rol


        # Verificar los filtros antes de hacer la llamada a la API
        print("Filtros enviados a la API:", filtros)


        # Traer los reportes desde la API
        respuesta = gestionar_reportes_admin(token, filtros)
        print("Reportes recibidos de la API:", respuesta)

        # Crear las tarjetas con la información obtenida
        tarjetas = []
        if respuesta.get("success") and "reportes" in respuesta:
            for reporte in respuesta["reportes"]:
                if isinstance(reporte, dict):
                    tarjetas.append(
                        tarjeta_reporte(
                            de=f"{reporte.get('reportador_nombre', 'N/A')}",
                            para=f"{reporte.get('reportado_nombre', 'N/A')}",
                            id_reporte=reporte.get('reporte_id', 'N/A'),
                            full_description=reporte.get('descripcion_reporte', 'N/A'),
                            rol_reportador = reporte.get("rol_reportador", "N/A"),
                            usuario_id = reporte.get("usuario_id_reportador", "N/A")
                        )
                    )
        return tarjetas

    def redirigir_por_rol(r, id,  page):

        #Redirige al perfil correcto según el rol del usuario.

        print(r)

        def accion(e):
            if r == "experto":
                page.usuario_id = id
                page.clean()
                perfil_experto.main(page)

            elif r == "cliente":
                page.usuario_id = id
                page.clean()
                perfil_usuario.main(page)

            else:
                print(f"Rol  no reconocido.")



        return accion





    def tarjeta_reporte(de, para, id_reporte, full_description, rol_reportador, usuario_id):
        display_description = full_description.split(' ... ')[0] if ' ... ' in full_description else full_description
        has_more = ' ... ' in full_description

        menu_desplegable = ft.PopupMenuButton(
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
                    on_click=lambda e, r=rol_reportador, id=usuario_id: redirigir_por_rol(r, id, page)(e)
                ),
            ],
        )

        return ft.Container(
            bgcolor="#FFFFFF",
            padding=20,
            content=ft.Column([
                # Encabezado
                ft.Row(
                    [
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(f"De: {de}", size=18,color="#333333", weight=ft.FontWeight.BOLD),
                                ft.Text(f"Para: {para}", size=18,color="#333333", weight=ft.FontWeight.BOLD),
                            ],
                        ),
                        ft.Row(
                            spacing=10,
                            controls=[
                                ft.Text("ID", color="#888888", size=18),
                                ft.Text(f"#{id_reporte}", color="#2FBDB3", weight=ft.FontWeight.BOLD, size=18),
                                menu_desplegable
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                # Descripción
                ft.Container(
                    bgcolor="#EEEEEE",
                    padding=ft.padding.all(10),
                    border_radius=5,
                    height=120,
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(display_description, color="#333333", size=18, max_lines=5,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Text("Ver más", color=ft.Colors.BLUE, size=18,
                                    italic=True) if has_more else ft.Container(),
                        ],
                    ),
                ),

                ft.Container(expand=True),  # Espaciador
            ],
                spacing=10,
                expand=True
            ),
            border_radius=8,
            border=ft.border.all(1, "#DDDDDD"),
            width=370,
            height=300,
        )



    # Solo una vez
    total_reportes_text = ft.Text(f"Total usuarios: 0", size=14, color=TEXT_COLOR)
    mensaje_error = ft.Text("", color=ft.Colors.RED)

    # Función para actualizar el total de reportes

    def actualizar_total_reportes(total_real):
        total_reportes_text.value = f"Total usuarios: {total_real}"
        total_reportes_text.update()



    def cargar_reportes_iniciales(page):
        global tarjetas_todas, tarjetas_actuales, start_index
        tarjetas_todas = obtener_reportes(page, None, None, None)  # sin filtros
        tarjetas_actuales = tarjetas_todas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(page, start_index, tarjetas_actuales)
        page.update()

    def aplicar_filtros(e):
        global tarjetas_filtradas, tarjetas_actuales, start_index
        reporte_id = id_reporte_field.value.strip() if id_reporte_field.value else None
        reportador_id = id_usuario_field.value.strip() if id_usuario_field.value else None
        rol = rol_dropdown.value.strip() if rol_dropdown.value else None


        if not reporte_id:
            reporte_id = None

        if not reportador_id:
            reportador_id = None

        if rol  == "Todas":
            rol = None

        print(f"ID REPORTE: {reporte_id},  ID REPORTADOR: {reportador_id}, ROL: {rol}")

        tarjetas_filtradas = obtener_reportes(e.page, reporte_id, reportador_id, rol)
        tarjetas_actuales = tarjetas_filtradas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(e.page, start_index, tarjetas_actuales)
        e.page.update()

    def eliminar_filtros(e):
        global tarjetas_todas, tarjetas_actuales, start_index

        tarjetas_todas = obtener_reportes(page, None, None, None)  # sin filtros

        tarjetas_actuales = tarjetas_todas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(e.page, start_index, tarjetas_actuales)
        e.page.update()

    filtros.content.controls.extend([
        ft.ElevatedButton(
            text="Aplicar filtros",
            icon=ft.Icons.FILTER_ALT,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                shape=ft.RoundedRectangleBorder(radius=20),
                side=ft.BorderSide(1, "#2FBDB3"), color="#333333",
            ),
            on_click=aplicar_filtros
        ),
        ft.ElevatedButton(
            text="Eliminar filtros",
            icon=ft.Icons.CLEAR,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                shape=ft.RoundedRectangleBorder(radius=20),
                side=ft.BorderSide(1, "#2FBDB3"), color="#333333",
            ),
            on_click=eliminar_filtros
        ),

    ])

    # Flechas
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

    # Navegación centrada con spacing dinámico
    navegacion = ft.Container(
        width=CAROUSEL_WIDTH,
        content=ft.Row(
            controls=[btn_prev, btn_next],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=ARROW_SPACING,
        ),
        padding=ft.padding.only(left=-35),
    )

    # Carrusel con tarjetas + navegación
    carrusel = ft.Column(
        controls=[tarjetas_container, navegacion],
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Contenedor del título
    titulo_container = ft.Container(
        content=ft.Text(
            "Todos los reportes",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR,
        ),
        alignment=ft.alignment.center,  # centrado
        padding=ft.padding.only(left=-355),
    )

    # Contenedor principal con título + carrusel
    reportes_list_container = ft.Container(
        content=ft.Column(
            controls=[
                titulo_container,
                carrusel,
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # centrado
        ),
        expand=True,
        padding=ft.padding.only(left=85, top=0),  # parecido al de usuarios
    )

    main_content = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    [filtros, total_reportes_text],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                ),
                margin=ft.margin.only(top=39),
                expand=False,
                alignment=ft.alignment.top_center,
            ),
            reportes_list_container,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=20,
    )

    page.add(header, tabs, main_content, confirm_dialog)

    # Cargar reportes iniciales **después** de agregar el control a la página
    cargar_reportes_iniciales(page)


if __name__ == "__main__":
    ft.app(target=main)
