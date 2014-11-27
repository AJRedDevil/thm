

from django import forms

from .models import Jobs

import logging
logger = logging.getLogger(__name__)

class JobCreationForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """

    class Meta:
        model = Jobs
        fields = ['jobtype','remarks','destination_home']