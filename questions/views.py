# questions/views.py
import json
import uuid
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Question, Answer


def parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid JSON")

@method_decorator(csrf_exempt, name='dispatch')
class QuestionListView(View):
    """GET /questions/ — список вопросов
       POST /questions/ — создать вопрос"""

    def get(self, request):
        questions = Question.objects.prefetch_related("answers").all()
        data = [
            {
                "id": q.id,
                "text": q.text,
                "created_at": q.created_at.isoformat(),
                "answers": [
                    {
                        "id": a.id,
                        "user_id": a.user_id,
                        "text": a.text,
                        "created_at": a.created_at.isoformat(),
                    }
                    for a in q.answers.all()
                ],
            }
            for q in questions
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            payload = parse_json_body(request)
        except ValueError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        text = payload.get("text", "").strip()
        if not text:
            return JsonResponse({"error": "text is required and cannot be empty"}, status=400)

        question = Question.objects.create(text=text)
        return JsonResponse(
            {
                "id": question.id,
                "text": question.text,
                "created_at": question.created_at.isoformat(),
            },
            status=201,
        )

@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetailView(View):
    """GET /questions/{id}/ — вопрос + ответы
       DELETE /questions/{id}/ — удалить вопрос (каскадно)"""

    def get(self, request, question_id):
        try:
            question = Question.objects.prefetch_related("answers").get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)

        data = {
            "id": question.id,
            "text": question.text,
            "created_at": question.created_at.isoformat(),
            "answers": [
                {
                    "id": a.id,
                    "user_id": a.user_id,
                    "text": a.text,
                    "created_at": a.created_at.isoformat(),
                }
                for a in question.answers.all()
            ],
        }
        return JsonResponse(data)

    def delete(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)

        question.delete()  # ← каскад сработает!
        return JsonResponse({"status": "deleted"}, status=204)

@method_decorator(csrf_exempt, name='dispatch')
class AnswerDetailView(View):
    """GET /answers/{id}/ — получить ответ
       DELETE /answers/{id}/ — удалить ответ"""

    def get(self, request, answer_id):
        try:
            answer = Answer.objects.select_related("question").get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({"error": "Answer not found"}, status=404)

        data = {
            "id": answer.id,
            "question_id": answer.question_id,
            "user_id": answer.user_id,
            "text": answer.text,
            "created_at": answer.created_at.isoformat(),
        }
        return JsonResponse(data)

    def delete(self, request, answer_id):
        try:
            answer = Answer.objects.get(id=answer_id)
        except Answer.DoesNotExist:
            return JsonResponse({"error": "Answer not found"}, status=404)

        answer.delete()
        return JsonResponse({"status": "deleted"}, status=204)

@method_decorator(csrf_exempt, name='dispatch')
class AnswerCreateView(View):
    """POST /questions/{id}/answers/ — добавить ответ"""

    def post(self, request, question_id):
        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({"error": "Question not found"}, status=404)

        try:
            payload = parse_json_body(request)
        except ValueError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        user_id = payload.get("user_id", "").strip()
        text = payload.get("text", "").strip()

        if not user_id:
            return JsonResponse({"error": "user_id is required"}, status=400)
        if not text:
            return JsonResponse({"error": "text is required and cannot be empty"}, status=400)

        try:
            uuid.UUID(user_id)
        except ValueError:
            return JsonResponse({"error": "user_id must be a valid UUID"}, status=400)

        answer = Answer.objects.create(
            question=question,
            user_id=user_id,
            text=text,
        )
        return JsonResponse(
            {
                "id": answer.id,
                "question_id": answer.question_id,
                "user_id": answer.user_id,
                "text": answer.text,
                "created_at": answer.created_at.isoformat(),
            },
            status=201,
        )