

from django.contrib.gis import forms
from django.utils.translation import ugettext_lazy as _
from .models import Jobs, JOBS_SELECTION
from users.models import UserProfile
from libs.googleapi_handler import GMapPointWidget
from moneyed import Money, NPR
import logging
logger = logging.getLogger(__name__)


class JobCreationForm(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """

    class Meta:
        model = Jobs
        fields = ['jobtype', 'remarks']

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)
        self.fields['jobtype'].widget.attrs={'class' : 'form-control'}
        self.fields['remarks'].widget.attrs={'class' : 'form-control'}


class JobCreationFormAdmin(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """

    class Meta:
        model = Jobs
        fields = ['customer','jobtype','remarks',
                    'location',]

    def __init__(self, *args, **kwargs):
        super(JobCreationFormAdmin, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs={'class' : 'form-control'}
        self.fields['jobtype'].widget.attrs={'class' : 'form-control'}
        self.fields['remarks'].widget.attrs={'class' : 'form-control','placeholder':'The flush is leaking!'}
        # gcoord = SpatialReference(4326)
        # mycoord = SpatialReference(900913)
        # trans = CoordTransform(gcoord, mycoord)
        # self.fields['location'].transform(trans)
        self.fields['location'].widget = GMapPointWidget(attrs={'map_width': 555, 'map_height': 500})
        self.fields['location'].widget.attrs={'class' : 'form-control'}


class JobEditFormAdmin(forms.ModelForm):
    """
    A form that creates a post, from the given data
    """
    error_messages = {
        'negative_currency': _("Fees can never be negative!"),
        'complete_job': _("Job once complete cannot be reverted"),
        }

    handyman = forms.ModelMultipleChoiceField(queryset=UserProfile.objects.filter(user_type=1, is_active=True),
                                              required=False)

    class Meta:
        model = Jobs
        fields = ['jobtype', 'remarks', 'fee', 'status', 'handyman',
        'location', 'location_landmark', 'inspection_date']


    def __init__(self, *args, **kwargs):
        super(JobEditFormAdmin, self).__init__(*args, **kwargs)
        self.fields['jobtype'].widget.attrs.update({'class' : 'form-control'})
        self.fields['remarks'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fee'].widget.attrs.update({'class' : 'form-control'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})
        self.fields['handyman'].widget.attrs.update({'class' : 'form-control ip-form'})
        self.fields['location'].widget = GMapPointWidget(attrs={'map_width': 750, 'map_height': 500})
        self.fields['location_landmark'].widget = forms.HiddenInput()
        self.fields['inspection_date'].widget.attrs.update({'class' : 'form-control', 'id' : 'inspection_date'})

    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee.amount < 0:
            raise forms.ValidationError(
            self.error_messages['negative_currency'],
            code='negative_currency'
            )

        return fee
