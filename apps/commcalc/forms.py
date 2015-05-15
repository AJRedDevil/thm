

from django import forms
from apps.users.models import UserProfile
import logging
logger = logging.getLogger(__name__)


class CommissionForm(forms.Form):
    """Form to handle the commission"""
    handyman = forms.ModelMultipleChoiceField(
        queryset=UserProfile.objects.filter(user_type=1, is_active=True))

    def __init__(self, *args, **kwargs):
        super(CommissionForm, self).__init__(*args, **kwargs)
        self.fields['handyman'].widget.attrs.update(
            {'class': 'form-control'})
