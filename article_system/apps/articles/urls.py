from django.urls import path
from .views import upload_article, upload_success, check_article_status,article_detail
app_name = 'articles'

urlpatterns = [
    path('', upload_article, name='home'),  # Ana sayfa = makale yükleme
    path('upload/', upload_article, name='upload_article'), 
    path('upload/success/<uuid:tracking_id>/', upload_success, name='upload_success'),  # 
    path('status/', check_article_status, name='check_article_status'),  
    path('article/<int:article_id>/', article_detail, name='article_detail'),  # ✅ Yeni URL
]
