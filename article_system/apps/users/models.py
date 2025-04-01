from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPES =[
        ('author','yazar'),
        ('editor','yönetici'),
        ('referee','hakem'),
    ]
    user_type=models.CharField(max_length=10,choices=USER_TYPES,default='author')
    
    def is_editor(self):
        return self.user_type=='editor'
    def is_referee(self):
        return self.user_type=='referee'
