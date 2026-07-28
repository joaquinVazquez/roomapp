import requests

BASE_URL = "http://127.0.0.1:8000"


def login():
    print("🔐 Intentando login...")

    url = f"{BASE_URL}/login"

    data = {
        "username": "juan@test.com",
        "password": "123456"
    }

    try:
        response = requests.post(url, data=data, timeout=5)
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None

    print("📡 Status:", response.status_code)
    print("📨 Response:", response.text)

    if response.status_code != 200:
        print("❌ Login falló")
        return None

    return response.json().get("access_token")


def test_mis_horarios():
    print("🚀 Ejecutando test...")

    token = login()

    if not token:
        print("❌ No se obtuvo token")
        return

    print("✅ Token obtenido")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/horarios/mis-horarios",
            headers=headers,
            timeout=5
        )
    except Exception as e:
        print("❌ Error al consultar horarios:", e)
        return

    print("\n📅 MIS HORARIOS")
    print("Status:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    print("📌 Iniciando script...")
    test_mis_horarios()