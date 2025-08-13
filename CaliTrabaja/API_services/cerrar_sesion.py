import requests

BASE_URL = "http://127.0.0.1:5000/api"

def cerrar_sesion_api():
    try:
        res = requests.post(f"{BASE_URL}/cerrar_sesion_admin")
        data = res.json()
        return data
    except Exception as e:
        return {"success":False,"message":f"Error de cerrar sesion: {str(e)}"}
