from django.db import models
from django.utils import timezone


class Question(models.Model):
    text = models.TextField()  
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Q{self.id}: {self.text[:30]}..."

    class Meta:
        ordering = ["-created_at"]


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,  
        related_name="answers"
    )
    user_id = models.CharField(max_length=36)  
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"A{self.id} (Q{self.question_id}) by {self.user_id[:8]}..."

    class Meta:
        ordering = ["created_at"]