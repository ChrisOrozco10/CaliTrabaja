import requests

BASE_URL = "http://127.0.0.1:5000"


def gestionar_publicaciones_admin(token, filtros=None):
    url = f"{BASE_URL}/api/gestion_publicaciones_admin"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.post(url, headers=headers, json=filtros if filtros else {})

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