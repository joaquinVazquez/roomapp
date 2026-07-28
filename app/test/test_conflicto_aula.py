import requests

BASE_URL = "http://127.0.0.1:8000"


def test_conflicto_aula():

    print("\n--- TEST CONFLICTO DE AULA ---")

    # ⚠️ IMPORTANTE:
    # Cambia este ID por el horario creado en el seed
    horario_id = 6  # ajusta según salida del seed

    response = requests.put(
        f"{BASE_URL}/horarios/{horario_id}/reasignar-aula?nueva_aula_id=2"
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)


if __name__ == "__main__":
    test_conflicto_aula()