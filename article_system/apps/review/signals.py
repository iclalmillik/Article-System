from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import CustomUser
from .models import Referee

@receiver(post_save, sender=CustomUser)
def create_referee(sender, instance, created, **kwargs):
    """
    Yeni bir CustomUser eklendiğinde eğer 'referee' rolünde ise Referee tablosuna ekler.
    """
    if created and instance.user_type == 'referee':  
                Referee.objects.create(user=instance, expertise="Uzmanlık Alanı Belirtilmedi")  # Varsayılan olarak boş bırakabiliriz




@receiver(post_save, sender=CustomUser)
def save_referee(sender, instance, **kwargs):
    """
    CustomUser güncellendiğinde eğer 'referee' rolündeyse Referee tablosundaki bilgilerini de günceller.
    """
    if hasattr(instance, 'referee') and instance.user_type == 'referee':  
        instance.referee.save()
