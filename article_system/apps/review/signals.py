from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import CustomUser
from .models import Referee

@receiver(post_save, sender=CustomUser)
def create_referee(sender, instance, created, **kwargs):
  
    if created and instance.user_type == 'referee':  
                Referee.objects.create(user=instance, expertise="No Area of ​​Expertise Specified")  




@receiver(post_save, sender=CustomUser)
def save_referee(sender, instance, **kwargs):
   
    if hasattr(instance, 'referee') and instance.user_type == 'referee':  
        instance.referee.save()
