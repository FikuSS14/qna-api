from django.urls import path
from .. import views

urlpatterns = [
    path("", views.QuestionListView.as_view(), name="question-list-create"),
    path("<int:question_id>/", views.QuestionDetailView.as_view(), name="question-detail"),
    path("<int:question_id>/answers/", views.AnswerCreateView.as_view(), name="answer-create"),
]