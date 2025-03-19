from pyexpat.errors import messages
from django.contrib import messages 
from django.shortcuts import get_object_or_404, redirect, render


from apps.users.models import CustomUser
from apps.review.forms import RefereeRegistrationForm


from .models import Referee,Review
from apps.articles.models import Article
from apps.review.models import Referee,Review

def is_admin(user):
    return user.is_superuser or user.is_staff


def editor_dashboard(request):
    
    articles = Article.objects.all().order_by('-submission_date')
   
      
    return render(request, 'review/editor_dashboard.html', {'articles': articles})

def referee_dashboard(request):
    return render(request, 'review/referee_dashboard.html')

def referee_register(request):
    if request.method == 'POST':
        form = RefereeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hakem başarıyla kaydedildi.')
            return redirect('review:referee_list')
    else:
        form = RefereeRegistrationForm()
    
    return render(request, 'review/referee_register.html', {'form': form})


def referee_list(request):
    referees = Referee.objects.all()
    return render(request, 'review/referee_list.html', {'referees': referees})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    referees = Referee.objects.all()  # Tüm hakemleri al

    return render(request, 'articles/article_detail.html', {
        'article': article,
        'referees': referees  # Şablona hakemleri gönderiyoruz
    })
    
    

def assign_referee(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        referee_id = request.POST.get('referee')
        if referee_id:
            referee = get_object_or_404(Referee, id=referee_id)
            
            # Hakemi makaleye atama
            article.referee_assignments.add(referee)
            
            # Yeni bir inceleme oluştur
            Review.objects.create(
                article=article,
                referee=referee,
                review_status='pending'
            )
            
            messages.success(request, f'Hakem {referee.user.get_full_name() or referee.user.username} başarıyla atandı.')
        else:
            messages.error(request, 'Lütfen bir hakem seçin.')
    
    return redirect('articles:article_detail', article_id=article_id)