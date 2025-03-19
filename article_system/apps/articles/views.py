from django.shortcuts import render, redirect,get_object_or_404

from apps.users.models import CustomUser
from apps.review.models import Referee
from .forms import ArticleUploadForm
from .models import Article  #  Modeli içe aktardık

#  Makale yükleme fonksiyonu
def upload_article(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article=form.save()
        return redirect('articles:upload_success', tracking_id=str(article.tracking_id))   # Başarıyla kaydedildiyse yönlendirme yap
    else:
        form = ArticleUploadForm()

    return render(request, 'articles/upload.html', {'form': form})  

def upload_success(request, tracking_id):
    article = get_object_or_404(Article, tracking_id=tracking_id)  # ✅ UUID'yi al
    return render(request, 'articles/upload_success.html', {'article': article})

# Makale durum sorgulama
def check_article_status(request):
    tracking_id = request.GET.get('tracking_id', None)
    email = request.GET.get('email', None)

    if tracking_id and email:
        try:
            article = Article.objects.get(tracking_id=tracking_id, author_email=email)
            return render(request, 'articles/status.html', {'article': article})
        except Article.DoesNotExist:
            return render(request, 'articles/status.html', {'error': 'Makale bulunamadı.'})

    return render(request, 'articles/status.html')
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    referees = Referee.objects.all()  # Tüm hakemleri getir
    
    context = {
        'article': article,
        'referees': referees,
    }
    
    return render(request, 'articles/article_detail.html', context)

#  Ana sayfa
def home(request):
    return render(request, 'articles/home.html') 
