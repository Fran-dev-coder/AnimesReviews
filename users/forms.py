from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
        labels = {
            'first_name':'Name',
        }

class ProfileForm(ModelForm):
    username = forms.CharField(max_length=150, required=True)
    
    class Meta:
        model = Profile
        fields = ['bio','profile_img']

    def __init__(self,*args,**kwargs):
        user = kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['username'].initial = user.username
        
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
            profile.save()
        return profile