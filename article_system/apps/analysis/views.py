from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Article
from .utils import extract_keywords, extract_text_from_pdf  # ✅ Eklediğimiz fonksiyonu içe aktar
def analyze_keywords(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    # PDF'ten metni çıkar
    pdf_text = extract_text_from_pdf(article.pdf_file.path)
    
    # Anahtar kelimeleri analiz et
    keywords = extract_keywords(pdf_text)

    return render(request, 'analysis/analyze_keywords.html', {'keywords': keywords, 'article': article})