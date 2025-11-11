from django.test import TestCase
from django.urls import reverse
import uuid


class QnaAPITestCase(TestCase):
    def test_cascade_delete_question_deletes_answers(self):
        """Проверка: при удалении вопроса удаляются все его ответы (каскадно)"""
        response = self.client.post(
            "/questions/",
            {"text": "Вопрос для удаления"},
            content_type="application/json",
        )
        question_id = response.json()["id"]
        user_id = str(uuid.uuid4())

        self.client.post(
            f"/questions/{question_id}/answers/",
            {"user_id": user_id, "text": "Ответ 1"},
            content_type="application/json",
        )
        self.client.post(
            f"/questions/{question_id}/answers/",
            {"user_id": user_id, "text": "Ответ 2"},
            content_type="application/json",
        )

        response = self.client.get(f"/questions/{question_id}/")
        answers = response.json()["answers"]
        self.assertEqual(len(answers), 2)

        self.client.delete(f"/questions/{question_id}/")

        response = self.client.get(f"/questions/{question_id}/")
        self.assertEqual(response.status_code, 404)

    def test_create_answer_to_nonexistent_question_fails(self):
        """Проверка: нельзя создать ответ к несуществующему вопросу"""
        response = self.client.post(
            "/questions/999/answers/",
            {"user_id": str(uuid.uuid4()), "text": "Тест"},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Question not found", str(response.content))