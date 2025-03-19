from django.db import models
from apps.articles.models import Article
from apps.users.models import CustomUser 


class Referee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255, blank=True, null=True)
    assigned_articles = models.ManyToManyField(Article, blank=True, related_name='referee_assignments')

    def __str__(self):
        return self.user.username
    
    
from apps.review.models import Referee 

class Review(models.Model):
    REVIEW_STATUS = [
        ('pending', 'Beklemede'),
        ('accepted', 'Kabul Edildi'),
        ('rejected', 'Reddedildi'),
        ('revision', 'Revize İstendi'),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='reviews')
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS, default='pending')
    comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} - {self.referee.user.username} ({self.review_status})"