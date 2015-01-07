from django import forms
from .models import FAQ

class FAQCreationForm(forms.ModelForm):
    """
    A form that helps create a FAQ
    """
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
