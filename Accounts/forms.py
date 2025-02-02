from django import forms
from allauth.account.forms import SignupForm
from .models import User,UserFavorites

# class UserCreationForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email','password']

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=50, label='Full Name')

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.save()
        return user
    
class UserDetailsUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['full_name','email','phone']

class UserFavoriteForm(forms.ModelForm):
    class Meta:
        model=UserFavorites
        exclude=["user","product"]