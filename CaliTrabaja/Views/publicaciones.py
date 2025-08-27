import flet as ft
import reportes
import crearADMIN
from flet import Icons, Colors
import datetime
import usuarios
import login
import inicio
import config_cuenta
import perfil_experto
import perfil_usuario
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.iniciar_admin import iniciar_sesion_api
from CaliTrabaja.API_services.obtener_publicaciones import gestionar_publicaciones_admin
from CaliTrabaja.API_services.eliminar_publicacion import desactivar_publicaciones

def main(page: ft.Page):
    global tarjetas_container, tarjetas


    def obtener_token(page):
        return getattr(page, "session_token", None)





    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")
    DESCRIPTION_BG = "#EEEEEE"
    PRIMARY_COLOR = "#2FBDB3"
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND = "#FFFFFF"
    BORDER_COLOR = "#DDDDDD"
    TEXT_COLOR = "#333333"
    DESCRIPTION_TEXT_COLOR = ft.Colors.BLACK54

    page.title = "CaliTrabaja - Publicaciones"
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
            height=110,  # ← AQUÍ MODIFICAS EL ALTO DEL MODAL
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
                color=TEXT_COLOR,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(width=2, color="#D9D9D9"),
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
                on_click=lambda e: cerrar_dialogo()
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # === FUNCIÓN PARA CERRAR EL DIALOGO ===
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
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
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
        #Configuracion
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=25,
        padding=5,
        #Re-cuadro
        margin=ft.margin.only(top=5, bottom=20, left=250, right=250),

    )

    def eliminar_publicaciones(id, page):
        token = obtener_token(page)

        if token is None:
            print("Token no valido, inicia sesion")

        datos = {}
        if id:
            datos["publicacion_id"] = id

        respuesta = desactivar_publicaciones(token, datos)
        print(respuesta)

        if respuesta.get("success") == True:
            print("Publicacion eliminada correctamente")

        else:
            print("Publicacion no eliminada")


        cargar_publicaciones_iniciales(page)
        page.update()


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







    def tarjeta_publicacion(id_publicacion,usuario_id, rol, nombre, descripcion, costo, categoria, estado_publicacion,  calificacion_estrellas=3):
        def get_stars(rating):
            return ft.Row(
                [
                    ft.Icon(
                        name=ft.Icons.STAR if i < rating else ft.Icons.STAR_BORDER,
                        color="#2FBDB3",
                        size=16
                    ) for i in range(5)
                ],
                spacing=1
            )

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
                    on_click=lambda e, r=rol, id=id_publicacion: redirigir_por_rol(r, id, page)(e)
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.REPORT_PROBLEM, color="#333333", size=20),
                            ft.Text("Notificar Problema", color="#333333"),
                        ],
                        spacing=10,
                    ),
                    on_click=lambda e: abrir_confirmacion(nombre, "notificar un problema", id_publicacion)
                ),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(name=ft.Icons.BLOCK, color="#333333", size=20),
                            ft.Text("Eliminar Publicacion", color="#333333"),
                        ],
                        spacing=10,
                    ),
                    on_click=lambda e, id=id_publicacion: eliminar_publicaciones( id, page)
                ),
            ],
        )

        return ft.Container(
            bgcolor="#FFFFFF",
            padding=ft.padding.only(left=15, right=15, top=10, bottom=10),
            content=ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Text(f"ID #{id_publicacion}", size=12, color="#333333"),
                            menu_desplegable,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Row(
                        spacing=10,
                        controls=[
                            ft.CircleAvatar(
                                radius=30,
                                content=ft.Icon(ft.Icons.PERSON, size=30, color=ft.Colors.WHITE),
                                color=ft.Colors.GREY_300
                            ),
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(nombre, size=16, weight=ft.FontWeight.BOLD, color="#333333"),
                                    get_stars(calificacion_estrellas),
                                ]
                            ),
                        ]
                    ),

                    ft.Column(
                        spacing=5,
                        controls=[
                            ft.Text("Descripción:", size=14, color="#333333", weight=ft.FontWeight.BOLD),
                            ft.Text(descripcion, size=12, color="#777777", max_lines=3,
                                    overflow=ft.TextOverflow.ELLIPSIS),
                        ]
                    ),

                    ft.Container(expand=True),

                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(f"COP {costo}/hr", size=14, weight=ft.FontWeight.BOLD, color="#777777"),
                            ft.Text(f"Categoría: {categoria}", size=12, color="#333333"),
                            ft.Text(f"Estado: {estado_publicacion}", size=12, color="#333333"),
                        ]
                    ),

                    ft.Container(
                        content=ft.ElevatedButton(
                            "Contactar experto",
                            bgcolor="#FFFFFF",
                            color="#333333",
                            style=ft.ButtonStyle(
                                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                                shape=ft.RoundedRectangleBorder(radius=20),
                                side=ft.BorderSide(1, "#2FBDB3"),
                            ),
                            width=220
                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=10)
                    ),
                ],
                spacing=8,
            ),
            border_radius=16,
            border=ft.border.all(1, "#DDDDDD"),
            width=280,
            height=390,
        )

    # 🔹 Controles de filtros
    id_publicacion_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)
    categoria_dropdown = ft.Dropdown(
        width=120,
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Reparación y Mantenimiento"),
            ft.dropdown.Option("Cuidado y Asistencia"),
            ft.dropdown.Option("Bienestar de Mascotas"),
            ft.dropdown.Option("Educativos y aprendizaje"),
            ft.dropdown.Option("Hogar y Limpieza"),
            ft.dropdown.Option("Construcción y Remodelación"),
            ft.dropdown.Option("Artísticos y creatividad visual"),
            ft.dropdown.Option("Movilidad y transporte"),
            ft.dropdown.Option("Gastronomía"),
            ft.dropdown.Option("Eventos"),
            ft.dropdown.Option("Bienestar Personal"),
        ],
        text_size=12,
        border_radius=5,
        value="Todas",
    )




    #-----------------------------------------------------------------

    # Contenedor para las tarjetas (inicialmente vacío)
    tarjetas_container = ft.Row(
        controls=[],  # Inicia el Row vacío
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        wrap=False,  # Cambié a True para que las tarjetas puedan ocupar varias filas si es necesario
        expand=True
    )



    #------------------------------------------------
    VISIBLE_CARDS = 2
    CARD_WIDTH = 280
    CARD_HEIGHT = 390
    CARD_SPACING = 10
    CAROUSEL_WIDTH = VISIBLE_CARDS * CARD_WIDTH + (VISIBLE_CARDS - 1) * CARD_SPACING

    def actualizar_tarjetas(page, start_index, tarjetas_lista):
        tarjetas_container.controls.clear()

        if not tarjetas_lista:
            # Mantener altura y ancho fijo para que el carrusel no se suba
            tarjetas_container.controls.append(
                ft.Container(
                    content=ft.Text("No hay publicaciones disponibles.", color="red"),
                    alignment=ft.alignment.center,
                    width=CAROUSEL_WIDTH,  # mismo ancho del carrusel
                    height=CARD_HEIGHT,  # misma altura de las tarjetas
                )
            )
            total_publicaciones = 0
        else:
            # Mostrar las visibles según el índice
            visibles = tarjetas_lista[start_index:start_index + VISIBLE_CARDS]
            tarjetas_container.controls.extend(visibles)
            total_publicaciones = len(tarjetas_lista)



        actualizar_total_publicaciones(total_publicaciones)
        page.update()

        # Funciones de paginación
    def siguiente(e):
        global start_index,  tarjetas_actuales

        if tarjetas_actuales:
            if start_index + VISIBLE_CARDS < len(tarjetas_actuales):  #  Avanzar normal
                start_index += VISIBLE_CARDS
            else:
                start_index = 0
            actualizar_tarjetas(e.page, start_index, tarjetas_actuales)

    def anterior(e):
        global start_index, tarjetas_actuales

        if tarjetas_actuales:
            if start_index - VISIBLE_CARDS >= 0:  # Retrocede normal
                start_index -= VISIBLE_CARDS
            else:
                start_index = max(0, len(tarjetas_actuales) - VISIBLE_CARDS)  # Va al final si retrocede demasiado

            #  siempre actualizar
            actualizar_tarjetas(e.page, start_index, tarjetas_actuales)


    def obtener_publicacion(page, id_pub=None, categoria=None):
        token =  obtener_token(page)
        if not token:
            page.add(ft.Text("Debe iniciar sesión primero"))
            return []

        # Construir los filtros dinámicamente
        filtros = {}
        if id_pub:
            filtros["publicacion_id"] = id_pub  # Solo agregamos el filtro si tiene valor
        if categoria and categoria != "Todas":
            filtros["tipo_categoria"] = categoria

        # Verificar los filtros antes de hacer la llamada a la API
        print(" Filtros enviados a la API:", filtros)

        # Llamar a la API para obtener las publicaciones
        respuesta = gestionar_publicaciones_admin(token, filtros)
        print("Publicaciones recibidas de la API:", respuesta)





        # Crear las tarjetas con la información obtenida
        tarjetas = []
        if respuesta.get("success") and "lista_publicaciones" in respuesta:
            for publicacion in respuesta["lista_publicaciones"]:
                if isinstance(publicacion, dict):
                    tarjetas.append(
                        tarjeta_publicacion(
                            nombre=f"{publicacion.get('primer_nombre', '')} {publicacion.get('primer_apellido', '')}",
                            id_publicacion=publicacion.get("publicacion_id", "N/A"),
                            rol = publicacion.get("rol", "N/A"),
                            usuario_id = publicacion.get("usuario_id", "N/A"),
                            descripcion=publicacion.get("descripcion_publicacion", "N/A"),
                            costo=publicacion.get("precio", "N/A"),
                            categoria=publicacion.get("nombre_subcategoria", "N/A"),
                            calificacion_estrellas=publicacion.get("calificacion_estrellas", 3),
                            estado_publicacion = publicacion.get("estado_publicacion", "N/A")
                        )
                    )
        return tarjetas






    #---------------------------------------------




    # Filtros
    id_publicacion_field = ft.TextField(label="ID publicación", width=120)
    categoria_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Reparación y Mantenimiento"),
            ft.dropdown.Option("Cuidado y Asistencia"),
            ft.dropdown.Option("Bienestar de Mascotas"),
            ft.dropdown.Option("Educativos y aprendizaje"),
            ft.dropdown.Option("Hogar y Limpieza"),
            ft.dropdown.Option("Construcción y Remodelación"),
            ft.dropdown.Option("Artísticos y creatividad visual"),
            ft.dropdown.Option("Movilidad y transporte"),
            ft.dropdown.Option("Gastronomía"),
            ft.dropdown.Option("Eventos"),
            ft.dropdown.Option("Bienestar Personal"),

        ],
        label="Categorías",
        width=120,
    )




    # Contenedor para los filtros
    filtros = ft.Container(
        content=ft.Column(
            [
                ft.Text("Filtrar por:", weight=ft.FontWeight.BOLD, size=14, color=TEXT_COLOR),
                ft.Row([  # Filtro de ID publicación
                    ft.Text("ID publicación", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    id_publicacion_field,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([  # Filtro de Categoría
                    ft.Text("Categorías", expand=True, color=TEXT_COLOR, size=14, weight=ft.FontWeight.BOLD),
                    categoria_dropdown,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ],
            spacing=8,
        ),
        padding=12,
        bgcolor=CARD_BACKGROUND,
        height=250,
        width=260,
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=ft.border_radius.all(16),
    )

    # Solo una vez
    total_publicaciones_text = ft.Text(f"Total publicaciones: 0", size=14, color=TEXT_COLOR)
    mensaje_error = ft.Text("", color=ft.Colors.RED)

    # Contenedor para las tarjetas
    publicaciones_list_containers = ft.Container(
        content=ft.Column(
            controls=[tarjetas_container, mensaje_error],
        ),
        expand=True,
        padding=ft.padding.only(left=20, top=0),
    )

    # Contenedor de paginación
    paginacion_controls = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.ARROW_BACK_IOS_NEW,
                on_click=anterior,
                icon_size=40,
                icon_color=PRIMARY_COLOR,
                tooltip="Anterior",
            ),
            ft.IconButton(
                icon=ft.Icons.ARROW_FORWARD_IOS,
                on_click=siguiente,
                icon_size=40,
                icon_color=PRIMARY_COLOR,
                tooltip="Siguiente",
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    # Contenedor para el título
    titulo_container = ft.Container(
        content=ft.Text(
            "Todas las publicaciones",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR,
        ),
        alignment=ft.alignment.center,  # Asegura que el título esté centrado
        padding=ft.padding.only(left=-300),  # Ajustar el padding
    )



    # Estructura final de la columna de publicaciones
    publicaciones_list_container = ft.Container(
        content=ft.Column(
            controls=[titulo_container, publicaciones_list_containers, paginacion_controls],
        ),
        expand=True,
        padding=ft.padding.only(left=20, top=0),
    )

    # -----------------------------

    # Función para actualizar el total de publicaciones
    def actualizar_total_publicaciones(total_real):
        total_publicaciones_text.value = f"Total publicaciones: {total_real}"
        total_publicaciones_text.update()

    def cargar_publicaciones_iniciales(page):
        global tarjetas_todas, tarjetas_actuales, start_index
        tarjetas_todas = obtener_publicacion(page, None, None)  # sin filtros
        tarjetas_actuales = tarjetas_todas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(page, start_index, tarjetas_actuales)
        page.update()




    def aplicar_filtros(e):
        global tarjetas_filtradas, tarjetas_actuales, start_index
        id_pub = id_publicacion_field.value.strip() if id_publicacion_field.value else None
        categoria = categoria_dropdown.value.strip() if categoria_dropdown.value else None


        if not id_pub:
            id_pub = None

        if categoria == "Todas":
            categoria = None

        print(f"ID: {id_pub}, Categoria: {categoria}")

        tarjetas_filtradas = obtener_publicacion(e.page, id_pub, categoria)
        tarjetas_actuales = tarjetas_filtradas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(e.page, start_index, tarjetas_actuales)
        e.page.update()

    def eliminar_filtros(e):
        global tarjetas_todas, tarjetas_actuales, start_index

        tarjetas_todas = obtener_publicacion(e.page, None, None)

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

    # Contenedor principal
    main_content = ft.Container(
        padding=ft.padding.only(top=20),  # altura general
        content=ft.Row(
            controls=[
                # FILTROS DE PUBLICACIONES
                ft.Container(
                    margin=ft.margin.only(top=40),  #  baja solo el menú de filtrar
                    content=ft.Column(
                        [filtros, total_publicaciones_text],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10
                    ),
                    expand=False,
                    alignment=ft.alignment.top_center,
                ),
                # TARJETAS DE PUBLICACIONES (el carrusel)
                publicaciones_list_container,
            ],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=20,
        )
    )

    page.add(header, tabs, main_content,confirm_dialog)

    # Cargar publicaciones iniciales **después** de agregar el control a la página
    cargar_publicaciones_iniciales(page)

if __name__ == "__main__":
    ft.app(target=main)
