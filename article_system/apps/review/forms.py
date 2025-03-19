from django import forms
from apps.users.models import CustomUser
from apps.review.models import Referee

class RefereeRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
   
    expertise = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Referee
        fields = ['expertise']

    def save(self, commit=True):
        # Önce CustomUser oluştur
        user_data = {
            'email': self.cleaned_data['email'],
            'username': self.cleaned_data['email'],  # Email'i username olarak kullan
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
             'user_type': 'referee', 
        }
        user = CustomUser.objects.create_user(**user_data)
       
        user.save()

        # Sonra Referee oluştur
        referee = super().save(commit=False)
        referee.user = user
        referee.expertise = self.cleaned_data['expertise']
        if commit:
            referee.save()
        return referee