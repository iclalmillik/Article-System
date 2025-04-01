
from django.contrib import messages 
from django.shortcuts import get_object_or_404, redirect, render
from apps.review.forms import RefereeRegistrationForm
from .models import Referee,Review
from apps.articles.models import Article, ArticleLog
from apps.review.models import Referee,Review

def is_admin(user):
    return user.is_superuser or user.is_staff


def editor_dashboard(request):
    
    articles = Article.objects.all().order_by('-submission_date')
    logs = ArticleLog.objects.all().order_by('-timestamp')
   
      
    return render(request, 'review/editor_dashboard.html', {'articles': articles , 'logs': logs})

def referee_dashboard(request):
    
    return render(request, 'review/referee_dashboard.html')

def referee_register(request):
    if request.method == 'POST':
        form = RefereeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Referee successfully registered.')
            return redirect('review:referee_list')
    else:
        form = RefereeRegistrationForm()
    
    return render(request, 'review/referee_register.html', {'form': form})


def referee_list(request):
    referees = Referee.objects.all()
    return render(request, 'review/referee_list.html', {'referees': referees})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    referees = Referee.objects.all()
    
 
    review = Review.objects.filter(article=article).first() 
    
    return render(request, 'articles/article_detail.html', {
        'article': article,
        'referees': referees,
        'review': review,  
    })

    

def assign_referee(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if article.referee_assignments.exists():
        messages.error(request, 'A referee has already been assigned to this article.')
        return redirect('articles:article_detail', article_id=article_id)
    
    if request.method == 'POST':
        referee_id = request.POST.get('referee')
        if referee_id:
            referee = get_object_or_404(Referee, id=referee_id)
            
          
            article.referee_assignments.add(referee)
            
          
            Review.objects.create(
                article=article,
                referee=referee,
                review_status='pending'
            )
            
           
            ArticleLog.objects.create(
                article=article,
                event='assigned',
                description=f"Referee {referee.user.get_full_name() or referee.user.username} has been appointed."
            )
            
            messages.success(request, f'Referee {referee.user.get_full_name() or referee.user.username} successfully appointed.')
        else:
            messages.error(request, 'Please choose a referee.')
    
    return redirect('articles:article_detail', article_id=article_id)

def referee_assigned_articles(request, referee_id):
    #  hakemi bul
    referee = get_object_or_404(Referee, id=referee_id)
    # hakeme atanan makaleleri çek
    assigned_articles = referee.assigned_articles.all()
    
    return render(request, 'review/referee_assigned_articles.html', {
        'referee': referee,
        'assigned_articles': assigned_articles,
    })

    
    
    
from django.contrib import messages
from apps.articles.models import Article
from apps.review.forms import ReviewForm  
from apps.review.models import Review

def submit_review(request, article_id, referee_id):
    # 1) Makale ve hakemi bul
    article = get_object_or_404(Article, id=article_id)
    referee = get_object_or_404(Referee, id=referee_id)
    
    
    review = Review.objects.filter(article=article, referee=referee).first()
    
    if request.method == 'POST':
    
        posted_referee_id = request.POST.get('referee_id')
        if str(referee.id) != posted_referee_id:
            messages.error(request, "Invalid referee information!")
            return redirect('articles:article_detail', article_id=article.id) 
        
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.article = article
            review.referee = referee
            review.save()
            
         
            ArticleLog.objects.create(
                article=article,
                event='replied',
                description=f"Referee {referee.user.get_full_name() or referee.user.username}submitted a review."
            )
            
            if review.review_status == 'approved':
                 article.review_status = 'Approved'
            elif review.review_status == 'rejected':
              article.review_status = 'Rejected'
            article.save()


            messages.success(request, "Your evaluation has been saved.")
            return redirect('review:referee_assigned_articles', referee_id=referee.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review/submit_review.html', {
        'article': article,
        'referee': referee,
        'form': form,
    })
    
    
 
from django.contrib import messages
from django.core.files.base import ContentFile
from apps.articles.models import Article
from apps.review.models import Review
from apps.articles.views import deanonymize_article



def process_review(request, article_id, review_id):
    
  review = get_object_or_404(Review, id=review_id)
  article = get_object_or_404(Article, id=article_id)
  
    
  if review.article.id != article.id:
        messages.error(request, "Review record does not belong to this article!")
        return redirect('review:editor_dashboard')  
    
  if request.method == 'POST':
    
        deanonymized_file = deanonymize_article(article)
        
        file_name = f"{article.id}_deanonymized.pdf"
        if not article.deanonymized_file:
            article.deanonymized_file.save(file_name, ContentFile(deanonymized_file.read()))
            article.save()
            
            
           
             
            if review.review_status == 'approved':
                 article.review_status = 'Approved'
            elif review.review_status == 'rejected':
              article.review_status = 'Rejected'
            article.save()


  
        review.editor_approved = True
        review.save()
            
            
             
        ArticleLog.objects.create(
            article=article,
            event='published',
            description=f"Approved by the editor: {article.review_status}."
        )
        
        
        messages.success(request,"The evaluation result was de-anonymized and forwarded to the author.")
        
       
        return render(request, 'review/process_review.html', {
            'article': article,
            'review': review,
        })
    
  return render(request, 'review/process_review.html', {
        'article': article,
        'review': review,
    }) 