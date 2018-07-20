from django import forms
from .models import Transgression

class TransgressionForm(forms.ModelForm):
    class Meta:
        model = Transgression
        fields = ['reason', 'banned_until']
        widgets = {
            'reason': forms.Textarea(),
            'banned_until': forms.DateTimeInput(),
        }

