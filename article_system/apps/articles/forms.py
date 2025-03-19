from django import forms 
from .models import Article
import re  # Regex için


# Makale sayısını kontrol et
print(Article.objects.count())

# Mevcut makaleleri listele
for article in Article.objects.all():
    print(article.title, article.author_email, article.pdf_file)
    
    

class ArticleUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'pdf_file', 'author_email']
        
        def clean_author_email(self):
            email = self.cleaned_data.get('author_email')
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, email):
                raise forms.ValidationError("Geçerli bir e-posta adresi giriniz!")
            return email