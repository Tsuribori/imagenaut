from django import forms
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from imageboard.models import Thread, Board


class ArchiveSearchForm(forms.Form):

    #Must recreate something akin to forms.SelectDateWidget(), which doesn't allow empty values in any field. 
    
    empty_choice = (None, '---------')
    month_choices = [empty_choice] + list(((str(x), x) for x in range(1,13)))
    day_choices =   [empty_choice] + list(((str(x), x) for x in range(1,33)))
    board = forms.ModelChoiceField(queryset=Board.objects.all(), to_field_name='name')
    year = forms.ChoiceField(required=False, choices=[])
    month = forms.ChoiceField(required=False, choices=month_choices)
    day = forms.ChoiceField(required=False, choices=day_choices)

    #Setting the year choices must be inside the __init__ method in order for the choices to be updated
    def __init__(self, *args, **kwargs):
        super(ArchiveSearchForm, self).__init__(*args, **kwargs)
        current_year = timezone.now().year
        try:
            last_thread = Thread.objects.filter(archived=True).earliest('time_made')
            last_year = last_thread.time_made.year
        except ObjectDoesNotExist:
            last_year = current_year
        year_choices = [(None, '---------')] + list(((str(x), x) for x in range(last_year, current_year + 1)))
        self.fields['year'].choices = year_choices
  

      
    def clean(self):
        data = self.cleaned_data
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        if day and not month:
            raise ValidationError('Month must be provided.')
        if month and not year:
            raise ValidationError('Year must be provided')

    
