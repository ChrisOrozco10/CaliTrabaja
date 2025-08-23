import requests

BASE_URL = "https://juan200521.pythonanywhere.com"

def cerrar_sesion_api():
    try:
        res = requests.post(f"{BASE_URL}/api/cerrar_sesion_admin")
        data = res.json()
        return data
    except Exception as e:
        return {"success":False,"message":f"Error de cerrar sesion: {str(e)}"}
