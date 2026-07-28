import requests

BASE_URL = "http://127.0.0.1:8000"


def test_docente():
    print("\n--- HORARIO POR DOCENTE ---")

    response = requests.get(
        f"{BASE_URL}/horarios/docente/2"
    )

    print(response.status_code)
    print(response.json())


def test_grupo():
    print("\n--- HORARIO POR GRUPO ---")

    response = requests.get(
        f"{BASE_URL}/horarios/grupo/1"
    )

    print(response.status_code)
    print(response.json())


def test_aula():
    print("\n--- HORARIO POR AULA ---")

    response = requests.get(
        f"{BASE_URL}/horarios/aula/1"
    )

    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    test_docente()
    test_grupo()
    test_aula()