from django.urls import path
from .. import views

urlpatterns = [
    path("<int:answer_id>/", views.AnswerDetailView.as_view(), name="answer-detail"),
]