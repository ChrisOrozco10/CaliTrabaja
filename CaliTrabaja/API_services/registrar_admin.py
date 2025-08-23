import requests

BASE_URL = "https://juan200521.pythonanywhere.com"

def registrar_sesion_api(correo):
    try:
        response = requests.post(
            f"{BASE_URL}/api/registrar_sesion_admin",
            json={"correo":correo}
        )
        return response.json()
    except Exception as e:
        return {"success":False,"message":f"Error de consulta: {e}"}
