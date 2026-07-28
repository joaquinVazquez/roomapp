import requests

BASE_URL = "http://127.0.0.1:8000"


def test_reasignar():

    print("\n--- REASIGNAR AULA ---")

    response = requests.put(
        f"{BASE_URL}/horarios/1/reasignar-aula?nueva_aula_id=999"
    )

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    test_reasignar()

    