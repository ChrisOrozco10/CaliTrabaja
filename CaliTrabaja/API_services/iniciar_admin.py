import requests


def iniciar_sesion_api(correo, contrasena):
    url = "https://juan200521.pythonanywhere.com/api/iniciar_sesion_admin"

    data = {"correo": correo, "contrasena": contrasena}
    response = requests.post(url, json=data)

    # Validar respuesta
    if response.status_code != 200:
        print("Error en la petición:", response.status_code, response.text)
        return None

    if not response.text:
        print("La API respondió vacío")
        return None

    try:
        resultado_json = response.json()  # <-- aquí se convierte a dict
        return resultado_json
    except Exception as e:
        print("Error al decodificar JSON:", e)
        return None

