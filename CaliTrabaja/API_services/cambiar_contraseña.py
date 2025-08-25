import requests

BASE_URL = "http://127.0.0.1:5000"

def cambiar_contraseña_admin(token, datos=None):
    url = f"{BASE_URL}/api//cambiar_contraseña_admin"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.post(url, headers=headers, json=datos if datos else {})

        try:
            resultado_json = response.json()  # Convierte la respuesta JSON a dict
        except Exception:
            resultado_json = {
                "success": False,
                "message": f"Respuesta no válida del servidor: {response.text}"
            }
        return resultado_json

    except Exception as e:
        # Ahora devolvemos un dict incluso si hay fallo de conexión
        return {"success": False, "message": f"Error de conexión: {e}"}

