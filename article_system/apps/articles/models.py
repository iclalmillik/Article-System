from django.db import models
import uuid

# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=300)
    pdf_file=models.FileField(upload_to='articles/')
    author_email=models.EmailField()
    submission_date=models.DateTimeField(auto_now_add=True)
    review_status=models.CharField(max_length=20,default='Pending') #reviewed,accapted,rejected
    tracking_id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False) #takip no
    
def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = str(uuid.uuid4().hex[:12]).upper()  # 📌 12 karakterlik benzersiz takip numarası
        super().save(*args, **kwargs)

def __str__(self):
        return f"{self.title} - {self.tracking_id}"