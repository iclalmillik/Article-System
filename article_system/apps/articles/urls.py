from django.urls import path


from .views import  editor_logs, track_article_view, upload_article, upload_revised_article, upload_success, check_article_status,article_detail
app_name = 'articles'



urlpatterns = [
    path('', upload_article, name='home'),
    path('upload/', upload_article, name='upload_article'), 
    path('upload/success/<uuid:tracking_id>/', upload_success, name='upload_success'),
    path('status/', check_article_status, name='check_article_status'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('track/', track_article_view, name='track_article'),
    path('editor/logs/', editor_logs, name='editor_logs'),
    path('upload-revised/<int:article_id>/', upload_revised_article, name='upload_revised'),
    



]