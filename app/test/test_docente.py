import requests
from test_auth import login

BASE_URL = "http://127.0.0.1:8000"


# login docente
headers = login(
    "docente.prueba@unisa.edu.mx",
    "123456"
)


print("\n--- MIS HORARIOS (DOCENTE) ---")


response = requests.get(
    f"{BASE_URL}/horarios/mis-horarios-docente",
    headers=headers
)


print(response.status_code)
print(response.json())