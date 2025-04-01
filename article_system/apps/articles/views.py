
from django.contrib import messages 
from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse
from apps.review.models import Referee
from .forms import ArticleUploadForm, RevisedUploadForm
from .models import Article, ArticleLog  


def upload_article(request):
    if request.method == 'POST':
        form = ArticleUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
          
            ArticleLog.objects.create(
                article=article,
                event='received',
                description=f" {article.title} uploaded on {article.submission_date:%d %b %Y %H:%M}  ."
            )
            return redirect('articles:upload_success', tracking_id=str(article.tracking_id))
        else:
            
            return render(request, 'articles/upload.html', {'form': form})
    else:
        form = ArticleUploadForm()
    
    return render(request, 'articles/upload.html', {'form': form})



def upload_revised_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = RevisedUploadForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Revised article uploaded successfully.")
        else:
            messages.error(request, "There was a problem with the upload.")
    
    tracking_id = request.POST.get("tracking_id")
    
    return redirect(f"{reverse('articles:track_article')}?tracking_id={tracking_id}")


def upload_success(request, tracking_id):
    article = get_object_or_404(Article, tracking_id=tracking_id) 
    return render(request, 'articles/upload_success.html', {'article': article})


def check_article_status(request):
    tracking_id = request.GET.get('tracking_id', None)
    email = request.GET.get('email', None)

    if tracking_id and email:
        try:
            article = Article.objects.get(tracking_id=tracking_id, author_email=email)
            return render(request, 'articles/status.html', {'article': article})
        except Article.DoesNotExist:
            return render(request, 'articles/status.html', {'error': 'No article found.'})

    return render(request, 'articles/status.html')

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
  
    reviews = article.reviews.all() 
    referees = Referee.objects.all()
   
    if request.method == 'POST':
        article.save()
    
        return redirect('review:article_detail', article_id=article.id)

    context = {
        'article': article,
        'reviews': reviews,
        'referees': referees,
      
    }
    return render(request, 'articles/article_detail.html', context)


def home(request):
    return render(request, 'articles/home.html') 


from apps.user_messages.forms import MessageForm  
from apps.user_messages.models import Message    
def track_article_view(request):
    tracking_id = request.POST.get('tracking_id') if request.method == 'POST' else None
    article = None
    searched = False
    form = MessageForm()

    if tracking_id:
        searched = True
        article = Article.objects.filter(tracking_id=tracking_id).first()

       
        if request.method == 'POST' and article:
            form = MessageForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.article = article
                message.sender_role = 'author'
                message.save()
                return redirect(request.path)  

    review_result = None
    if article:
        review_result = article.reviews.filter(editor_approved=True).first()
    if article:
        revised_form = RevisedUploadForm()
    else:
        revised_form = None
    
    return render(request, 'articles/track_article.html', {
        'article': article,
        'searched': searched,
        'tracking_id': tracking_id,
        'form': form,
        'user_messages': article.messages.all().order_by('timestamp') if article else [],
        'review_result': review_result,
        'revised_form': revised_form,
    })


def deanonymize_article(article):
   
    return article.pdf_file  



def editor_logs(request):
    logs = ArticleLog.objects.all().order_by('-timestamp')
    return render(request, 'articles/editor_logs.html', {'logs': logs})



