from django.utils import timezone
from django.db import models
from apps.articles.models import Article
from apps.users.models import CustomUser 


class Referee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=255, blank=True, null=True)
    assigned_articles = models.ManyToManyField(Article, blank=True, related_name='referee_assignments')

    def __str__(self):
        return self.user.username
    
 

class Review(models.Model):
    REVIEW_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    referee = models.ForeignKey(Referee, on_delete=models.CASCADE, related_name='reviews')
    review_status = models.CharField(max_length=20, choices=REVIEW_STATUS_CHOICES, default='pending')
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    editor_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.article.title} - {self.referee.user.username}"

    def save(self, *args, **kwargs):
        if self.review_status in ['approved', 'rejected'] and not self.reviewed_at:
            self.reviewed_at = timezone.now()
        super().save(*args, **kwargs)