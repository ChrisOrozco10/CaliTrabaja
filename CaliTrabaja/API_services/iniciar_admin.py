import requests

BASE_URL = "http://127.0.0.1:5000/api"

def iniciar_sesion_api(correo, contrasena):
    try:
        response = requests.post(
            f"{BASE_URL}/iniciar_sesion_admin",
            json={"correo": correo, "contrasena": contrasena}
        )
        return response.json()
    except Exception as e:
        return {"success": False, "message": f"Error de conexión: {e}"}
