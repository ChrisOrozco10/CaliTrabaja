import requests


BASE_URL = "https://juan200521.pythonanywhere.com"

def gestionar_reportes_admin(token, filtros=None):
    url = f"{BASE_URL}/api/gestion_reportes_admin"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    try:
        response = requests.post(url, headers=headers, json=filtros if filtros else {})
        # Verificar que la respuesta no esté vacía
        if response.status_code != 200 or not response.text:
            print("Error al conectar con la API o respuesta vacía")
            return []

        resultado = response.json()

        if not resultado.get("success", False):
            print("Error al obtener usuarios:", resultado.get("message"))
            return []

        return resultado.get("reportes", [])

    except requests.exceptions.RequestException as e:
        print("Error de conexión con la API:", e)
        return []
    except ValueError as e:  # Captura JSONDecodeError
        print("Error al decodificar JSON:", e)
        return []

