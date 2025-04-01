from .import views
from django.urls import path
from .views import assign_referee, editor_dashboard, article_detail, process_review, referee_assigned_articles, submit_review

app_name = 'review'

urlpatterns = [
path('yonetici/', editor_dashboard, name='editor_dashboard'),  
path('referee/dashboard/', views.referee_dashboard, name='referee_dashboard'),
path('referee/<int:referee_id>/assigned_articles/', referee_assigned_articles, name='referee_assigned_articles'),
path('article/<int:article_id>/', article_detail, name='article_detail'),  
path('article/<int:article_id>/assign/', assign_referee, name='assign_referee'),
path('referee/list/', views.referee_list, name='referee_list'), 
path('referee/register/', views.referee_register, name='referee_register'),
path('submit_review/<int:article_id>/<int:referee_id>/', submit_review, name='submit_review'),
path('process_review/<int:article_id>/<int:review_id>/', process_review, name='process_review'),

   
   
     
]
  
