import requests

BASE_URL = "http://127.0.0.1:5000/api"


def gestionar_publicaciones_admin(token):
    url = f"{BASE_URL}/gestion_publicaciones_admin"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.post(url, headers=headers)
        # Verificar que la respuesta no esté vacía
        if response.status_code != 200 or not response.text:
            print("Error al conectar con la API o respuesta vacía")
            return []
        resultado = response.json()  # Convierte la respuesta JSON a dict

        if not resultado.get("success", False):
            print("Error al obtener usuarios:", resultado.get("message"))
            return []

        return resultado.get("lista_publicaciones", [])

    except requests.exceptions.RequestException as e:
        print("Error de conexión con la API:", e)
        return []
    except ValueError as e:  # Captura JSONDecodeError
        print("Error al decodificar JSON:", e)
        return []