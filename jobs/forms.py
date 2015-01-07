

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Jobs

from moneyed import Money, NPR
import logging
logger = logging.getLogger(__name__)

class JobCreationForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """

    class Meta:
        model = Jobs
        fields = ['jobtype','remarks','destination_home']


class JobCreationFormAdmin(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """

    class Meta:
        model = Jobs
        fields = ['customer','jobtype','remarks','destination_home',
                    'remarks',]


class JobEditFormAdmin(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    error_messages = {
        'negative_currency': _("Fees can never be negative!"),
        }
        
    class Meta:
        model = Jobs
        fields = ['customer','jobtype','remarks','destination_home',
                    'remarks','fee','status','handyman','isaccepted','isnotified',
                    'completion_date',]

    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee.amount < 0:
            raise forms.ValidationError(
            self.error_messages['negative_currency'],
            code='negative_currency'
            )

        return fee
