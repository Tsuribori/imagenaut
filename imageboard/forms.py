from django import forms
from django.core.exceptions import ValidationError
from sorl.thumbnail.fields import ImageFormField 
from .models import Thread, UserPost
from .utils import GetIPMixin, CooldownMixin 
    
class ThreadForm(forms.ModelForm, GetIPMixin, CooldownMixin):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ThreadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Thread
        fields = ['subject', 'name', 'post', 'image', 'embed']
        widgets = {
            'post': forms.Textarea(),
        }

    
    def clean_name(self):
        name = self.cleaned_data['name']
        if self.user_on_cooldown(Thread):
            raise ValidationError('You must wait longer before making a new thread.')
        return name

class UserPostForm(forms.ModelForm, GetIPMixin, CooldownMixin):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserPostForm, self).__init__(*args, **kwargs)

    ModelInstance = Thread
    
    class Meta:
        model = UserPost
        fields = ['name', 'sage', 'post', 'image', 'embed']
        widgets = {
            'post': forms.Textarea(),
        }
       
  
    def clean_name(self):
        name = self.cleaned_data['name']
        if self.user_on_cooldown(UserPost):
            raise ValidationError('You must wait longer before making a new post.')
        return name
