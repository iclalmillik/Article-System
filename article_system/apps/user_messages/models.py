from django.db import models
from apps.articles.models import Article

class Message(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='messages')
    sender_role = models.CharField(max_length=10, choices=[('author', 'Author'), ('editor', 'Editor')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_role} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

