# qna/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("questions/", include("questions.urls.questions")),  
    path("answers/", include("questions.urls.answers")),     
]