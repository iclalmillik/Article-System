from django.urls import path
from .views import analyze_keywords  # ✅ Eklediğimiz view fonksiyonunu içe aktar

app_name = "analysis"  # ✅ Burada namespace tanımlandı

urlpatterns = [
    path('analyze_keywords/<int:article_id>/', analyze_keywords, name='analyze_keywords'),
]
