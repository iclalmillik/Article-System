from django.shortcuts import render, get_object_or_404, redirect
from .models import Message
from .forms import MessageForm
from apps.articles.models import Article


def author_message_view(request):
    tracking_id = request.GET.get('tracking_id')
    article = get_object_or_404(Article, tracking_id=tracking_id)
    messages_qs = article.messages.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.article = article
            message.sender_role = 'author'
            message.save()
            return redirect(request.path + f'?tracking_id={tracking_id}')
    else:
        form = MessageForm()

    return render(request, 'user_messages/author_message.html', {
        'article': article,
        'user_messages': messages_qs,
        'form': form,
    })

    
    

def editor_message_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    messages_qs = article.messages.all().order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.article = article
            msg.sender_role = 'editor'
            msg.save()
        return redirect('user_messages:editor_message', article_id=article.id)
    else:
        form = MessageForm()

    return render(request, 'user_messages/editor_message.html', {
        'article': article,
        'messages': messages_qs,
        'form': form,
    })
