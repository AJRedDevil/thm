

from django import forms
from .models import PricingModel
import logging
logger = logging.getLogger(__name__)

class PricingForm(forms.ModelForm):
    """Form to handle the estimated price"""

    error_messages = {
        "positive_num" : "Please enter counting numbers"
    }

    class Meta:
        model = PricingModel
        fields = ['time_unit_selection', 'estimated_time', 'complexity', 'discount']

    def __init__(self, *args, **kwargs):
        super(PricingForm, self).__init__(*args, **kwargs)
        self.fields['time_unit_selection'].widget.attrs.update({'class':'form-control'})
        self.fields['estimated_time'].widget.attrs.update({'class':'form-control'})
        self.fields['complexity'].widget.attrs.update({'class':'form-control'})
        self.fields['discount'].widget.attrs.update({'class':'form-control'})

    def clean(self):
        estimated_time = self.cleaned_data.get("estimated_time")
        if int(estimated_time) < 1:
            raise forms.ValidationError(
                self.error_messages['positive_num'], 
                code='positive_num'
                )

        complexity = self.cleaned_data.get("complexity")
        if (int(complexity)+1) < 1:
            raise forms.ValidationError(
                self.error_messages['positive_num'],
                code='positive_num'
                )

        return self.cleaned_data
