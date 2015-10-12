

import logging
from django.contrib.gis import forms
from django.utils.translation import ugettext_lazy as _
from libs.googleapi_handler import GMapPointWidget
from moneyed import Money, NPR

from .models import Jobs, JOBS_SELECTION, JobScheduler
from apps.subscription.models import Subscriber
from apps.users.models import UserProfile




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
        fields = ['jobtype', 'remarks', 'fee', 'is_paid', 'status', 'handyman',
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

class JobSchedulerInspectionForm(forms.ModelForm):
    """Form for creating Job Scheduler model
    """
    error_messages = {
        'emptyInspection':_("You must either submit both the start and end date inspection or None"),
        'pastInspection':_("Inspection end date cannot have past value than start date"),
    }

    class Meta:
        model = JobScheduler
        fields = ['inspection_start_date', 'inspection_end_date']

    def __init__(self, *args, **kwargs):
        super(JobSchedulerInspectionForm, self).__init__(*args, **kwargs)
        self.fields['inspection_start_date'].widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M')
        self.fields['inspection_start_date'].widget.attrs.update({'class' : 'form-control datetimepicker'})
        self.fields['inspection_start_date'].input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M']
        self.fields['inspection_end_date'].widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M')
        self.fields['inspection_end_date'].widget.attrs.update({'class' : 'form-control datetimepicker'})
        self.fields['inspection_end_date'].input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M']

    def clean(self):
        cleaned_data = super(JobSchedulerInspectionForm, self).clean()
        inspection_start_date = cleaned_data.get('inspection_start_date')
        inspection_end_date=cleaned_data.get('inspection_end_date')
        if (inspection_start_date and not inspection_end_date) or (not inspection_start_date and inspection_end_date):
            raise forms.ValidationError(
                self.error_messages['emptyInspection'],
                code='emptyInspection'
                )
        elif inspection_end_date < inspection_start_date:
            raise forms.ValidationError(
                self.error_messages['pastInspection'],
                code='pastInspection'
                )
        return cleaned_data


class JobSchedulerCompleteForm(forms.ModelForm):
    """Form for editing Job Scheduler model
    """
    error_messages = {
        'emptyInspection':_("You must either submit both the start and end date inspection or None"),
        'emptyJobTime':_("You must either submit both the start and end date job time or None"),
        'fillBoth':_("You must fill the inspection dates to enter the Job time"),
        'pastInspection':_("Inspection end date cannot have past value than start date"),
        'pastJobTime':_("Job end date cannot have past value than start date"),
        'past':_("Job cannot have past value than inspection date")

    }

    class Meta:
        model = JobScheduler
        exclude = ['active', 'job']

    def __init__(self, *args, **kwargs):
        super(JobSchedulerCompleteForm, self).__init__(*args, **kwargs)
        self.fields['inspection_start_date'].widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M')
        self.fields['inspection_start_date'].widget.attrs.update({'class' : 'form-control datetimepicker'})
        self.fields['inspection_start_date'].input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M']
        self.fields['inspection_end_date'].widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M')
        self.fields['inspection_end_date'].widget.attrs.update({'class' : 'form-control datetimepicker'})
        self.fields['inspection_end_date'].input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M']
        self.fields['job_start_date'].widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M')
        self.fields['job_start_date'].widget.attrs.update({'class' : 'form-control datetimepicker'})
        self.fields['job_start_date'].input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M']
        self.fields['job_end_date'].widget=forms.DateTimeInput(format='%Y/%m/%d %H:%M')
        self.fields['job_end_date'].widget.attrs.update({'class' : 'form-control datetimepicker'})
        self.fields['job_end_date'].input_formats=['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M']

    def clean(self):
        cleaned_data = super(JobSchedulerCompleteForm, self).clean()
        inspection_start_date = cleaned_data.get('inspection_start_date')
        inspection_end_date = cleaned_data.get('inspection_end_date')
        job_start_date = cleaned_data.get('job_start_date')
        job_end_date = cleaned_data.get('job_end_date')

        if (inspection_start_date and not inspection_end_date) or ( not inspection_start_date and inspection_end_date):
            raise forms.ValidationError(
                self.error_messages['emptyInspection'],
                code='emptyInspection'
                )
        elif (job_start_date and not job_end_date) or (not job_start_date and job_end_date):
            raise forms.ValidationError(
                self.error_messages['emptyJobTime'],
                code='emptyJobTime'
                )
        elif job_start_date and job_end_date and (not inspection_start_date or not inspection_end_date):
            raise forms.ValidationError(
                self.error_messages['emptyJobTime'],
                code='emptyJobTime'
                )
        elif inspection_end_date < inspection_start_date:
            raise forms.ValidationError(
                self.error_messages['pastInspection'],
                code='pastInspection'
                )
        elif job_end_date < job_start_date:
            raise forms.ValidationError(
                self.error_messages['pastJobTime'],
                code='pastJobTime'
                )
        elif (job_start_date < inspection_end_date or job_end_date < inspection_end_date):
            raise forms.ValidationError(
                self.error_messages['past'],
                code='past'
                )
        return cleaned_data

