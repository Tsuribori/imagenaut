from django import forms
from django.core.exceptions import ValidationError
#from sorl.thumbnail.fields import ImageFormField 
from captcha.fields import CaptchaField
from .models import Thread, UserPost
from .utils import GetIPMixin, CooldownMixin, MakeTripcode
    
class ThreadForm(forms.ModelForm, GetIPMixin, CooldownMixin, MakeTripcode):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ThreadForm, self).__init__(*args, **kwargs)
    
    captcha = CaptchaField()
    class Meta:
        model = Thread
        fields = ['subject', 'name', 'post', 'image', 'embed', 'id_enabled']
        widgets = {
            'post': forms.Textarea(),
        }

    
    def clean_name(self):
        name = self.cleaned_data['name']
        name = self.create_tripcode(name)
        if self.user_on_cooldown(Thread):
            raise ValidationError('You must wait longer before making a new thread.')
        return name

class UserPostForm(forms.ModelForm, GetIPMixin, CooldownMixin, MakeTripcode):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserPostForm, self).__init__(*args, **kwargs)

    captcha = CaptchaField()    
    class Meta:
        model = UserPost
        fields = ['name', 'sage', 'post', 'image', 'embed']
        widgets = {
            'post': forms.Textarea(),
        }
       
  
    def clean_name(self):
        name = self.cleaned_data['name']
        name = self.create_tripcode(name)
        if self.user_on_cooldown(UserPost):
            raise ValidationError('You must wait longer before making a new post.')
        return name
