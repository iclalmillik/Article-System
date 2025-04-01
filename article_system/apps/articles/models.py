import os
import shutil
from django.db import models
import uuid
from apps.analysis.models import SubjectArea  

class Article(models.Model):
    title = models.CharField(max_length=300)
    pdf_file = models.FileField(upload_to='articles/', null=True, blank=True)
    revised_file = models.FileField(upload_to='revised_pdfs/', null=True, blank=True)
    author_email = models.EmailField(verbose_name="E-Mail", blank=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    review_status = models.CharField(max_length=20, default='Pending') 
    tracking_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    subject_area = models.ForeignKey(
        SubjectArea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )

    anonymized_file = models.FileField(upload_to='anonymized_pdfs/', null=True, blank=True)
    deanonymized_file = models.FileField(upload_to='deanonymized_pdfs/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = str(uuid.uuid4().hex[:12]).upper()

        try:
            old = Article.objects.get(pk=self.pk)

         
            if self.revised_file and old.pdf_file:
              
                if os.path.isfile(old.pdf_file.path):
                    os.remove(old.pdf_file.path)

             
                if not self.revised_file.name.startswith('revised_pdfs/'):
                    self.revised_file.name = f"revised_pdfs/{self.revised_file.name}"

               
                new_filename = os.path.basename(self.revised_file.name)
                full_old_path = os.path.join('media', self.revised_file.name)
                new_path = os.path.join('media/articles/', new_filename)

                print(" Taşımaya çalışılan:", full_old_path)
                print(" Yeni konum:", new_path)

                if os.path.exists(full_old_path):
                    shutil.move(full_old_path, new_path)
                    print(" Dosya başarıyla taşındı.")
                    self.pdf_file.name = f'articles/{new_filename}'
                    self.revised_file = None
                else:
                    print(" Taşınacak dosya bulunamadı:", full_old_path)

        except Article.DoesNotExist:
            pass

        super().save(*args, **kwargs)
        
        
        
        
        
    def __str__(self):
        return f"{self.title} - {self.tracking_id}"

    def get_pdf_url(self):
        if self.pdf_file:
            return self.pdf_file.url
        return None
  
  
class ArticleLog(models.Model):
    EVENT_CHOICES = (
        ('received', 'Article Arrived'),
        ('assigned', 'Assigned to Referee'),
        ('replied', 'The Referee Responded'),
        ('published', 'It was published'),
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='logs')
    event = models.CharField(max_length=20, choices=EVENT_CHOICES)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article.title} - {self.get_event_display()} at {self.timestamp:%d %b %Y %H:%M}"