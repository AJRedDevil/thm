from django import forms
from .models import FAQ

class FAQCreationForm(forms.ModelForm):
    """
    A form that helps create a FAQ
    """
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

    def __init__(self, *args, **kwargs):
        super(FAQCreationForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs={'class':'form-control'}
        self.fields['answer'].widget.attrs={'class':'form-control'}