from django.urls import path
from .views import author_message_view, editor_message_view

app_name = "user_messages"

urlpatterns = [
    path('author/', author_message_view, name='author_message'),
    path('editor/<int:article_id>/', editor_message_view, name='editor_message'),
    
]
