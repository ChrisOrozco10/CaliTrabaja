import flet as ft
import reportes
import crearADMIN
import publicaciones
import login
import inicio
import config_cuenta
import perfil_experto
import perfil_usuario
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.obtener_usuarios import gestionar_usuarios_admin
from CaliTrabaja.API_services.deshabilitar_cuenta_global import deshabilitar_cuenta_global


def main(page: ft.Page):
    global  tarjetas_container, tarjetas

    def obtener_token(page):
        return getattr(page, "session_token", None)



    # -------------------- Tema y colores ----------------------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    page.theme = ft.Theme(font_family="Oswald")

    PRIMARY_COLOR    = "#2FBDB3"     # ← Color turquesa (flechas y otros elementos)
    BACKGROUND_COLOR = "#FAFAFA"
    CARD_BACKGROUND  = "#FFFFFF"
    BORDER_COLOR     = "#DDDDDD"
    TEXT_COLOR       = "#333333"

    # -------------------- Config. de ventana ------------------------------
    page.title            = "CaliTrabaja - Usuarios"
    page.window_maximized = True
    page.bgcolor          = BACKGROUND_COLOR
    page.padding          = 20

    # -------------------- Drawer ------------------------------------------
    def close_drawer(e):
        page.drawer.open = False
        page.update()

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
                        on_click= cerrar_sesion
                    )
                ),
            ],
        ),
    )

    # -------------------- Pestañas ----------------------------------------
    tabs = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Row(
            controls=[
                ft.TextButton(
                    text="Usuarios",
                    style=ft.ButtonStyle(
                        color=PRIMARY_COLOR,
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
        border=ft.border.all(1, BORDER_COLOR),
        border_radius=25,
        padding=5,
        margin=ft.margin.only(top=5, bottom=20, left=250, right=250),
    )
    # ---------------- Variables de los filtros ----------------
    id_usuario_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)
    nombre_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)
    apellido_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)
    correo_field = ft.TextField(width=120, height=35, text_size=12, border_radius=5)

    rol_dropdown = ft.Dropdown(
        width=120, text_size=12, border_radius=5, value="Todos",
        options=[ft.dropdown.Option(o) for o in ["Todos", "experto", "cliente", "admin"]],
    )

    estado_dropdown = ft.Dropdown(
        width=120, text_size=12, border_radius=5, value="Todos",
        options=[ft.dropdown.Option(o) for o in ["Todos", "activo", "deshabilitado"]],
    )

    publicaciones_dropdown = ft.Dropdown(
        width=120, text_size=12, border_radius=5, value="Todas",
        options=[ft.dropdown.Option(o) for o in ["Todas", "1", "2"]],
    )

    categorias_dropdown = ft.Dropdown(
        width=120, text_size=12, border_radius=5, value="Todas",
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
    )

    def deshabilitar_cuenta(id, page):

        token = obtener_token(page)
        if token is None:
            print("Token no valido, inicia sesion")

        datos = {}

        if id:
            datos["usuario_id"]= id


        respuesta =   deshabilitar_cuenta_global(token, datos)

        print(respuesta)

        if respuesta.get("success") == True:
            print("Usuario deshabilitado correctamente")

        else :
            print("Error al deshabilitar usuario")

        cargar_usuarios_iniciales(page)
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

    def tarjeta_usuario(nombre, rol, categoria, estado, fecha, correo, id_user, publicaciones, reportes, rating=3):


        controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text(nombre, size=20, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.PopupMenuButton(
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
                                on_click= lambda e, r= rol, id=id_user :redirigir_por_rol(r,id, page)(e)
                            ),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.REPORT_PROBLEM, color="#333333", size=20),
                                        ft.Text("Notificar Problema", color="#333333"),
                                    ],
                                    spacing=10,
                                ),
                                on_click=lambda e: abrir_confirmacion(nombre, "notificar un problema", id_user)
                            ),
                            ft.PopupMenuItem(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(name=ft.Icons.BLOCK, color="#333333", size=20),
                                        ft.Text("Deshabilitar Cuenta", color="#333333"),
                                    ],
                                    spacing=10,
                                ),
                                on_click=lambda e,  id=id_user: deshabilitar_cuenta( id, page)
                            ),
                        ],
                    )
                ]
            ),
            ft.Text(f"Rol: {rol}", size=18, color="#333333"),
            ft.Text(f"Estado: {estado}", size=18, color="#333333"),
            ft.Text(f"Se unió el {fecha}", size=18, color="#333333"),
            ft.Text(f"Correo: {correo}", size=18, color="#333333"),
            ft.Text(f"ID: {id_user}", size=18, color="#333333"),
        ]

        if rol:
            controls.insert(1, ft.Row([
                ft.Icon(ft.Icons.STAR if i < rating else ft.Icons.STAR_BORDER, color="#2FBDB3", size=24)
                for i in range(5)
            ]))
            controls.insert(2, ft.Text(f"Categoría: {categoria}", size=18, color="#333333"))

        return ft.Container(
            bgcolor="#FFFFFF",
            padding=30,
            content=ft.Column(
                spacing=10,
                controls=controls
            ),
            border_radius=10,
            border=ft.border.all(1, "#DDDDDD"),
            height=400,
            width=380,
        )
        # -----------------------------------------------------------------

        # Contenedor para las tarjetas (inicialmente vacío)

    tarjetas_container = ft.Row(
        controls=[],  # Inicia el Row vacío
        spacing=10,
        alignment=ft.MainAxisAlignment.START,
        wrap=False,  # Cambié a True para que las tarjetas puedan ocupar varias filas si es necesario
        expand=True
    )


    CARD_WIDTH =380
    CARD_SPACING = 20
    VISIBLE_CARDS = 2
    CAROUSEL_WIDTH = VISIBLE_CARDS * CARD_WIDTH + (VISIBLE_CARDS - 1) * CARD_SPACING

    # Distancia exacta entre flechas (una tarjeta + su separación)
    ARROW_SPACING = CARD_WIDTH + CARD_SPACING  # 300 px

    tarjetas_todas = []
    tarjetas_filtradas = []
    tarjetas_actuales = []  # <- Lista activa
    start_index = 0

    def actualizar_tarjetas(page, start_index, tarjetas_lista):
        tarjetas_container.controls.clear()

        if not tarjetas_lista:
            # Mantener altura y ancho fijo para que el carrusel no se suba
            tarjetas_container.controls.append(
                ft.Container(
                    content=ft.Text("No hay usuarios disponibles.", color="red"),
                    alignment=ft.alignment.center,
                    width=CAROUSEL_WIDTH,  # mismo ancho del carrusel
                    height=400,  # misma altura de las tarjetas
                )
            )
            total_usuarios = 0
        else:
            # Mostrar las visibles según el índice
            visibles = tarjetas_lista[start_index:start_index + VISIBLE_CARDS]
            tarjetas_container.controls.extend(visibles)
            total_usuarios = len(tarjetas_lista)

        actualizar_total_usuarios(total_usuarios)
        page.update()

    def siguiente(e):
        global start_index, tarjetas_actuales

        if tarjetas_actuales:
            if start_index + VISIBLE_CARDS < len(tarjetas_actuales):  #  Avanzar normal
                start_index += VISIBLE_CARDS
            else:
                start_index = 0
            actualizar_tarjetas(e.page, start_index, tarjetas_actuales)

    def anterior(e):
        global start_index, tarjetas_actuales

        if tarjetas_actuales:
            if start_index - VISIBLE_CARDS >= 0:  #  Retrocede normal
                start_index -= VISIBLE_CARDS
            else:
                start_index = max(0, len(tarjetas_actuales) - VISIBLE_CARDS)  #  Va al final si retrocede demasiado

            #  siempre actualizar
            actualizar_tarjetas(e.page, start_index, tarjetas_actuales)

    def obtener_usuario(page, id_usu=None, nombre=None,apellido=None, correo=None, rol=None, estado=None, categoria= None, publicaciones=None ):
        # Obtener el token de la sesión

        token = obtener_token(page)



        if not token:
            page.add(ft.Text("Debe iniciar sesión primero"))
            return

        filtros = {}
        if id_usu:
            filtros["usuario_id"] = id_usu
        if nombre:
            filtros["primer_nombre"] = nombre
        if apellido:
            filtros["primer_apellido"] = apellido
        if correo:
            filtros["correo"] = correo
        if rol and rol != "Todos":
            filtros["tipo_rol"] = rol
        if estado and estado != "Todos":
            filtros["estado"] = estado

        if publicaciones and publicaciones != "Todos":
            filtros["destacada"] = publicaciones

        if categoria and categoria != "Todas":
            filtros["tipo_categoria"] = categoria

        # Verificar los filtros antes de hacer la llamada a la API
        print(" Filtros enviados a la API:", filtros)


        # Traer los usuarios desde la API
        respuesta = gestionar_usuarios_admin(token, filtros)
        print("Usuarios recibidos de la API:", respuesta)

        # Crear las tarjetas con la información obtenida
        tarjetas = []
        if respuesta.get("success") and "usuarios" in respuesta:
            for usuario in respuesta["usuarios"]:
                # Si usuario es un diccionario, usamos .get(), si no, asumimos que es un string
                if isinstance(usuario, dict):
                    tarjetas.append(
                        tarjeta_usuario(
                            id_user=f"{usuario.get('usuario_id', 'N/A')}",
                            nombre=f"{usuario.get('primer_nombre', '')} {usuario.get('primer_apellido', '')}",
                            rol=usuario.get('tipo_rol', 'N/A'),
                            estado=usuario.get('estado', 'N/A'),
                            fecha=usuario.get('fecha_registro', 'N/A'),
                            correo=usuario.get('correo', 'N/A'),
                            publicaciones=usuario.get('publicaciones', 0),
                            reportes=usuario.get('reportes', 0),
                            categoria = ", ".join(usuario.get('categorias', [])) if usuario.get('categorias') else "N/A"
                        )
                    )
        return tarjetas

    #------------------------------------------------------------


    filtros = ft.Container(
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text("Filtrar por:", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR),

                    # --- ID usuario ---
                    ft.Row(
                        controls=[
                            ft.Text("ID usuario", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            id_usuario_field,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # --- Nombre ---
                    ft.Row(
                        controls=[
                            ft.Text("Nombre", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            nombre_field,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # --- Apellido ---
                    ft.Row(
                        controls=[
                            ft.Text("Apellido", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            apellido_field,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # --- Correo ---
                    ft.Row(
                        controls=[
                            ft.Text("Correo", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            correo_field,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # --- Rol ---
                    ft.Row(
                        controls=[
                            ft.Text("Rol", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            rol_dropdown,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # --- Estado ---
                    ft.Row(
                        controls=[
                            ft.Text("Estado", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            estado_dropdown,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),

                    # --- Publicaciones ---
                    ft.Row(
                        controls=[
                            ft.Text("Publicaciones", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            publicaciones_dropdown,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    # --- Categorías ---
                    ft.Row(
                        controls=[
                            ft.Text("Categorías", size=14, weight=ft.FontWeight.BOLD, color=TEXT_COLOR, expand=True),
                            categorias_dropdown
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
            padding=10,
            bgcolor=CARD_BACKGROUND,
            width=260,
            border=ft.border.all(1, BORDER_COLOR),
            border_radius=ft.border_radius.all(16),
        )

    # Solo una vez
    total_usuarios_text = ft.Text(f"Total usuarios: 0", size=14, color=TEXT_COLOR)
    mensaje_error = ft.Text("", color=ft.Colors.RED)







    # Flechas en color PRIMARY_COLOR y con icon_size 40 px
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

    # Navegación centrada y con spacing exacto
    navegacion = ft.Container(
        width=CAROUSEL_WIDTH,
        content=ft.Row(
            controls=[btn_prev, btn_next],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=ARROW_SPACING,
        ),
        padding=ft.padding.only(left=5),
    )

    carrusel = ft.Column(
        controls=[tarjetas_container, navegacion],
        spacing=25,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    # Contenedor para el título
    titulo_container = ft.Container(
        content=ft.Text(
            "Todos los usuarios",
            size=22,
            weight=ft.FontWeight.BOLD,
            color=PRIMARY_COLOR,
        ),
        alignment=ft.alignment.center,  # Asegura que el título esté centrado
        padding=ft.padding.only(left=-300),  # Ajustar el padding
    )

    # Estructura final de la columna de publicaciones
    usuarios_list_container = ft.Container(
        content=ft.Column(
            controls=[titulo_container, carrusel],
        ),
        expand=True,
        padding=ft.padding.only(left=20, top=0),
    )



    # Función para actualizar el total de publicaciones
    def actualizar_total_usuarios(total_real):
        total_usuarios_text.value = f"Total usuarios: {total_real}"
        total_usuarios_text.update()

    def cargar_usuarios_iniciales(page):
        global tarjetas_todas, tarjetas_actuales, start_index
        tarjetas_todas = obtener_usuario(page, None, None, None, None, None, None, None, None)  # sin filtros
        tarjetas_actuales = tarjetas_todas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(page, start_index, tarjetas_actuales)
        page.update()


    def aplicar_filtros(e):
        global tarjetas_filtradas, tarjetas_actuales, start_index
        id_usu = id_usuario_field.value.strip() if id_usuario_field.value else None
        nombre = nombre_field.value.strip() if nombre_field.value else None
        apellido = apellido_field.value.strip() if apellido_field.value else None
        correo = correo_field.value.strip() if correo_field.value else None
        rol = rol_dropdown.value.strip() if rol_dropdown.value else None
        estado = estado_dropdown.value.strip() if estado_dropdown.value else None
        publicaciones= publicaciones_dropdown.value.strip() if publicaciones_dropdown.value else None
        categoria = categorias_dropdown.value.strip() if categorias_dropdown.value else None



        if not id_usu:
            id_usu = None

        if not nombre:
            nombre = None

        if not apellido:
            apellido = None

        if not correo:
            correo = None

        if rol == "Todas":
            rol = None

        if estado == "Todos":
            estado = None

        if publicaciones == "Todas":
            publicaciones = None


        if categoria == "Todas":
            categoria = None

        print(f"ID: {id_usu}, Nombre: {nombre}, Apellido: {apellido}, Correo: {correo}, Rol: {rol}, Estado: {estado}, Publicaciones: {publicaciones} Categoria: {categoria}")

        tarjetas_filtradas = obtener_usuario(e.page, id_usu, nombre, apellido, correo, rol, estado, categoria, publicaciones)
        tarjetas_actuales = tarjetas_filtradas
        start_index = 0

        # Limpiar el contenedor de tarjetas
        tarjetas_container.controls.clear()

        # Renderizar usando la función de mostrar tarjetas
        actualizar_tarjetas(e.page, start_index, tarjetas_actuales)
        e.page.update()

    def eliminar_filtros(e):
        global tarjetas_todas, tarjetas_actuales, start_index

        tarjetas_todas = tarjetas_todas = obtener_usuario(page, None, None, None, None, None, None, None, None)  # sin filtros
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
            on_click=eliminar_filtros,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=15, vertical=10),
                shape=ft.RoundedRectangleBorder(radius=20),
                side=ft.BorderSide(1, "#2FBDB3"),color="#333333",
            ),
        ),
    ])


    # -------------------- Contenido principal ------------------------------

    # Contenedor principal
    main_content = ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    [filtros, total_usuarios_text],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10
                ),
                margin=ft.margin.only(top=39),  #  ajusta este valor (10–30) según se vea mejor
                expand=False,
                alignment=ft.alignment.top_center,
            ),
            usuarios_list_container,
        ],
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=20,
    )

    page.add(header, tabs, main_content,confirm_dialog)

    # Cargar usuarios iniciales **después** de agregar el control a la página
    cargar_usuarios_iniciales(page)


if __name__ == "__main__":
    ft.app(target=main)
