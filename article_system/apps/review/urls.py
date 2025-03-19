from .import views
from django.urls import path
from .views import assign_referee, editor_dashboard, article_detail, referee_dashboard

app_name = 'review'

urlpatterns = [
path('yonetici/', editor_dashboard, name='editor_dashboard'),  # Yönetici Paneli
path('referee/dashboard/', views.referee_dashboard, name='referee_dashboard'),
path('article/<int:article_id>/', article_detail, name='article_detail'),  
path('article/<int:article_id>/assign/', assign_referee, name='assign_referee'),
path('referee/list/', views.referee_list, name='referee_list'), 
path('referee/register/', views.referee_register, name='referee_register'),
   
     
]
  
