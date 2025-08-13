import requests

BASE_URL = "http://127.0.0.1:5000/api"

def registrar_sesion_api(correo):
    try:
        response = requests.post(
            f"{BASE_URL}/registrar_sesion_admin",
            json={"correo":correo}
        )
        return response.json()
    except Exception as e:
        return {"success":False,"message":f"Error de consulta: {e}"}
