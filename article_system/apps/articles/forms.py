from django import forms 
from .models import Article
import re  # regex





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
     
     
class RevisedUploadForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['revised_file']
