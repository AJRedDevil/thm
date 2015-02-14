

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Jobs
from users.models import UserProfile

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
        'complete_job': _("Job once complete cannot be reverted"),
        }

    handyman = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(user_type=1), required=False)

    class Meta:
        model = Jobs
        fields = ['customer','jobtype','remarks','destination_home',
                    'remarks','fee','status','handyman',]


    def __init__(self, *args, **kwargs):
        super(JobEditFormAdmin, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs.update({'class' : 'form-control'})
        self.fields['jobtype'].widget.attrs.update({'class' : 'form-control'})
        self.fields['remarks'].widget.attrs.update({'class' : 'form-control'})
        self.fields['destination_home'].widget.attrs.update({'class' : 'checkbox'})
        self.fields['fee'].widget.attrs.update({'class' : 'form-control col-sm-6 col-xs-6'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})
        self.fields['handyman'].widget.attrs.update({'class' : 'form-control ip-form'})
    
    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee.amount < 0:
            raise forms.ValidationError(
            self.error_messages['negative_currency'],
            code='negative_currency'
            )

        return fee
