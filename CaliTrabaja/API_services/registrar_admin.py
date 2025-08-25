import requests



def registrar_sesion_api(correo):
    url = "http://127.0.0.1:5000api/registrar_sesion_admin"
    data = {"correo": correo}

    try:
        response = requests.post(url, json=data)

        try:
            resultado_json = response.json()  # <-- aquí se convierte a dict
        except Exception:
            resultado_json = {
                "success": False,
                "message": f"Respuesta no válida del servidor: {response.text}"
            }
        return resultado_json

    except Exception as e:
        # Ahora devolvemos un dict incluso si hay fallo de conexión
        return {"success": False, "message": f"Error de conexión: {e}"}

