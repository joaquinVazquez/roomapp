import requests
from test_auth import login

BASE_URL = "http://127.0.0.1:8000"

headers = login("admin@test.com", "123456")

data = {
    "actividad_academica_id": 1,
    "dia_semana_id": 2,
    "hora_inicio": "10:00",
    "hora_fin": "11:00",
    "aula_id": 1
}

print("\n--- CREAR HORARIO ---")

response = requests.post(
    f"{BASE_URL}/horarios/",
    json=data,
    headers=headers
)

print(response.status_code)
print(response.json())