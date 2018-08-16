from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Transgression


class TransgressionForm(forms.ModelForm):
    class Meta:
        model = Transgression
        fields = ['reason', 'banned_until', 'global_ban']
        widgets = {
            'reason': forms.Textarea(),
            'banned_until': forms.DateTimeInput(),
        }

    def clean_banned_until(self):
        ban_time = self.cleaned_data['banned_until']
        if ban_time < timezone.now():
            raise ValidationError('Ban cannot expire in the past!')
        return ban_time

        
