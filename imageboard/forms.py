from django import forms
from .models import Thread, UserPost

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['subject', 'name', 'post']
        widgets = {
            'post': forms.Textarea(),
        }

class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['name', 'post']
        widgets = {
            'post': forms.Textarea(),
        }
       
   
