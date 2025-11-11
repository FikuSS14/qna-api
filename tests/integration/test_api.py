import requests
import uuid

BASE_URL = "http://localhost:8000"

def test_full_flow():
    # 1. Создать вопрос
    res = requests.post(f"{BASE_URL}/questions/", json={"text": "Тест"})
    assert res.status_code == 201
    question_id = res.json()["id"]

    # 2. Добавить ответ
    res = requests.post(
        f"{BASE_URL}/questions/{question_id}/answers/",
        json={"user_id": str(uuid.uuid4()), "text": "Ответ"}
    )
    assert res.status_code == 201

    # 3. Удалить вопрос
    res = requests.delete(f"{BASE_URL}/questions/{question_id}/")
    assert res.status_code == 204

    # 4. Проверить 404
    res = requests.get(f"{BASE_URL}/questions/{question_id}/")
    assert res.status_code == 404