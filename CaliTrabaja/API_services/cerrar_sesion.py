import requests

BASE_URL = "http://127.0.0.1:5000"

def cerrar_sesion_api(token=None):
    url = f"{BASE_URL}/api/cerrar_sesion_admin"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        res = requests.post(url, headers=headers)
        data  = res.json()
        return data
    except Exception as e:
        return {"success":False,"message":f"Error de cerrar sesion: {str(e)}"}