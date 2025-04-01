from django.urls import  path


from .views import analyze_keywords, anonymization_pdf

app_name = "analysis"  

urlpatterns = [
    
    path('analyze_keywords/<int:article_id>/', analyze_keywords, name='analyze_keywords'),
    path('anonymization_pdf/<int:article_id>/', anonymization_pdf, name='anonymization_pdf'),
   


]
