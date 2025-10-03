import flet as ft
import inicio
import login
import crearADMIN
import config_cuenta
from CaliTrabaja.API_services.cerrar_sesion import cerrar_sesion_api
from CaliTrabaja.API_services.cambiar_contraseña import cambiar_contraseña_admin

def main(page: ft.Page):
    # ---------------------- CONFIGURACIÓN DE LA PÁGINA ----------------------
    page.clean()
    page.fonts = {
        "Oswald": "https://raw.githubusercontent.com/google/fonts/main/ofl/oswald/Oswald%5Bwght%5D.ttf"
    }
    PRIMARY_COLOR = "#2FBDB3"
    TEXT_COLOR = "#333333"
    page.bgcolor = "white"

    #------------- OBTENER TOKEN--------------------
    def obtener_token(page):
        return getattr(page, "session_token", None)

    # ---------------------- FUNCIONES AUXILIARES ----------------------
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

    # ---------------------- CAMBIO DE CONTRASEÑA ----------------------
    def cambiar_contraseña(page, actual_contrasena, nueva_contrasena, confirmar_contrasena):
        token = obtener_token(page)
        if not token:
            page.add(ft.Text("Debes iniciar sesion primero"))
            return []

        datos = {}
        if actual_contrasena:
            datos["actual_contrasena"] = actual_contrasena
        if nueva_contrasena:
            datos["nueva_contrasena"] = nueva_contrasena
        if confirmar_contrasena:
            datos["confirmar_contrasena"] = confirmar_contrasena

        respuesta = cambiar_contraseña_admin(token, datos)
        if respuesta.get("success") == True:
            inicio.main(page)
        return respuesta

    def guardar_contraseña(e):
        contraseña_actual = contraseña_actual_field.value.strip() if contraseña_actual_field.value else None
        nueva_contraseña = nueva_contraseña_field.value.strip() if nueva_contraseña_field.value else None
        repetir_contraseña = repetir_contraseña_field.value.strip() if repetir_contraseña_field.value else None

        # Verificar que todas las reglas se cumplan y que coincidan las contraseñas
        if not todas_reglas_ok():
            mostrar_snackbar("La nueva contraseña no cumple las reglas de seguridad", exito=False)
            return

        if nueva_contraseña != repetir_contraseña:
            mostrar_snackbar("Las contraseñas no coinciden", exito=False)
            return

        respuesta = cambiar_contraseña(page, contraseña_actual, nueva_contraseña, repetir_contraseña)

        if respuesta.get("success"):
            mostrar_snackbar("Contraseña cambiada correctamente ", exito=True)
            page.clean()
            config_cuenta.main(page)
        else:
            mostrar_snackbar(respuesta.get("message", "Error al cambiar la contraseña"), exito=False)

    # ---------------------- CAMPOS ----------------------
    contraseña_actual_field = ft.TextField(password=True, can_reveal_password=True, border_radius=8, bgcolor="#E0E0E0", width=600)
    nueva_contraseña_field = ft.TextField(password=True, can_reveal_password=True, border_radius=8, bgcolor="#E0E0E0", width=600)
    repetir_contraseña_field = ft.TextField(password=True, can_reveal_password=True, border_radius=8, bgcolor="#E0E0E0", width=600)

    # ---------------------- VALIDACIONES DE CONTRASEÑA ----------------------
    regla_6_icon = ft.Icon(name=ft.Icons.HIGHLIGHT_OFF, color="red", size=18)
    regla_6_text = ft.Text("Al menos 6 caracteres", size=14)

    regla_mayus_icon = ft.Icon(name=ft.Icons.HIGHLIGHT_OFF, color="red", size=18)
    regla_mayus_text = ft.Text("Al menos 1 letra mayúscula", size=14)


    reglas_columna = ft.Column(
        spacing=5,
        controls=[
            ft.Row([regla_6_icon, regla_6_text]),
            ft.Row([regla_mayus_icon, regla_mayus_text]),
        ]
    )

    # --- confirmación (repetir contraseña) ---
    confirm_icon = ft.Icon(size=18)
    confirm_text = ft.Text("", size=14)
    confirm_row = ft.Row([confirm_icon, confirm_text], alignment=ft.MainAxisAlignment.START)

    def validar_password(e=None):
        pwd = nueva_contraseña_field.value or ""

        # longitud
        if len(pwd) >= 6:
            regla_6_icon.name, regla_6_icon.color = ft.Icons.CHECK_CIRCLE, "green"
        else:
            regla_6_icon.name, regla_6_icon.color = ft.Icons.HIGHLIGHT_OFF, "red"

        # mayúscula
        import re
        if re.search(r"[A-Z]", pwd):
            regla_mayus_icon.name, regla_mayus_icon.color = ft.Icons.CHECK_CIRCLE, "green"
        else:
            regla_mayus_icon.name, regla_mayus_icon.color = ft.Icons.HIGHLIGHT_OFF, "red"

        # también validar confirmación (por si el usuario cambia la nueva contraseña después de haber escrito la confirmación)
        validar_confirmacion()

        page.update()

    def validar_confirmacion(e=None):
        pwd = nueva_contraseña_field.value or ""
        confirm = repetir_contraseña_field.value or ""
        if confirm == "":
            confirm_text.value = ""
            confirm_icon.name = None
            confirm_icon.color = None
        elif pwd == confirm:
            confirm_icon.name = ft.Icons.CHECK_CIRCLE
            confirm_icon.color = "green"
            confirm_text.value = "Las contraseñas coinciden"
        else:
            confirm_icon.name = ft.Icons.HIGHLIGHT_OFF
            confirm_icon.color = "red"
            confirm_text.value = "Las contraseñas no coinciden"
        page.update()

    # Comprobar si todas las reglas (longitud, mayúscula y número) están OK
    def todas_reglas_ok():
        pwd = nueva_contraseña_field.value or ""
        import re
        return (
            len(pwd) >= 6 and
            bool(re.search(r"[A-Z]", pwd)) and
            bool(re.search(r"[0-9]", pwd))
        )

    nueva_contraseña_field.on_change = validar_password
    repetir_contraseña_field.on_change = validar_confirmacion

    # ---------------------- CONTENIDO ----------------------
    contenido = ft.Row(
        alignment="center",
        controls=[
            ft.Container(
                width=600,
                margin=ft.margin.only(top=50),
                content=ft.Column(
                    spacing=12,
                    horizontal_alignment="start",
                    controls=[
                        ft.Text("Cambiar contraseña", size=22, weight="bold", color="#3EAEB1", font_family="Oswald"),

                        ft.Text("Contraseña actual", size=18, color="black", font_family="Oswald"),
                        contraseña_actual_field,

                        ft.Text("Nueva contraseña", size=18, color="black", font_family="Oswald"),
                        nueva_contraseña_field,
                        reglas_columna,  # ⬅️ Reglas debajo del campo nueva contraseña

                        ft.Text("Repetir contraseña", size=18, color="black", font_family="Oswald"),
                        repetir_contraseña_field,
                        confirm_row,  # ⬅️ Indicador de coincidencia debajo de repetir contraseña

                        ft.Row(
                            alignment="start",
                            spacing=20,
                            controls=[
                                ft.ElevatedButton(
                                    "Cancelar",
                                    bgcolor="#F5F5F5",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=30),
                                        side=ft.BorderSide(width=2, color="#D9D9D9"),
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                        text_style=ft.TextStyle(font_family="Oswald", size=18),
                                    ),
                                    on_click=lambda e: (page.clean(), config_cuenta.main(page))
                                ),
                                ft.ElevatedButton(
                                    "Guardar cambios",
                                    bgcolor="#F5F5F5",
                                    color="black",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                        side=ft.BorderSide(width=2, color="#2FBDB3"),
                                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                                        text_style=ft.TextStyle(font_family="Oswald", size=18),
                                    ),
                                    on_click=guardar_contraseña
                                ),
                            ]
                        ),
                    ]
                )
            )
        ]
    )

    # ---------------------- LAYOUT ----------------------
    page.add(
        ft.Column(
            expand=True,
            controls=[
                header,
                contenido,
                ft.Container(expand=True, alignment=ft.alignment.top_left, padding=ft.padding.all(40)),
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
