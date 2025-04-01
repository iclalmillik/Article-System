from django import forms
from apps.users.models import CustomUser
from apps.review.models import Referee
from django import forms
from .models import Review

class RefereeRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
   
    expertise = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Referee
        fields = ['expertise']

    def save(self, commit=True):
        
        user_data = {
            'email': self.cleaned_data['email'],
            'username': self.cleaned_data['email'],  
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'user_type': 'referee', 
        }
        user = CustomUser.objects.create_user(**user_data)
       
        user.save()

      
        referee = super().save(commit=False)
        referee.user = user
        referee.expertise = self.cleaned_data['expertise']
        if commit:
            referee.save()
        return referee
    
    
    
    
    


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_status', 'rating', 'comments']
        widgets = {
            'review_status': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'placeholder': '1-10 arası puan'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional explanations...'
            }),
        }
