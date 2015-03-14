

from django.contrib.gis import forms
import floppyforms as floppyforms

# class GMapPointWidget(floppyforms.gis.PointWidget, floppyforms.gis.BaseGMapWidget):
    # pass

class GMapPointWidget(floppyforms.gis.BaseGeometryWidget):
    map_width = 800
    map_heght = 500
    map_srid = 900913  # Use the google projection
    template_name = 'google_map.html'
    is_point = True

    class Media:
        js = (
            'http://openlayers.org/api/2.13/OpenLayers.js',
            'floppyforms/js/MapWidget.js',
            '//maps.google.com/maps/api/js?v=3&sensor=false&libraries=places',
        )

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
                    'location',]

    def __init__(self, *args, **kwargs):
        super(JobCreationFormAdmin, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs={'class' : 'form-control'}
        self.fields['jobtype'].widget.attrs={'class' : 'form-control'}
        self.fields['remarks'].widget.attrs={'class' : 'form-control','placeholder':'The flush is leaking!'}
        self.fields['destination_home'].attrs={'class' : 'form-control'}
        # gcoord = SpatialReference(4326)
        # mycoord = SpatialReference(900913)
        # trans = CoordTransform(gcoord, mycoord)
        # self.fields['location'].transform(trans)
        self.fields['location'].widget = GMapPointWidget(attrs={'map_width': 800, 'map_height': 500})

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
        fields = ['customer','jobtype','remarks','destination_home',
                    'remarks','fee','status','handyman','location',]


    def __init__(self, *args, **kwargs):
        super(JobEditFormAdmin, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs.update({'class' : 'form-control'})
        self.fields['jobtype'].widget.attrs.update({'class' : 'form-control'})
        self.fields['remarks'].widget.attrs.update({'class' : 'form-control'})
        self.fields['destination_home'].widget.attrs.update({'class' : 'checkbox'})
        self.fields['fee'].widget.attrs.update({'class' : 'form-control col-sm-6 col-xs-6'})
        self.fields['status'].widget.attrs.update({'class' : 'form-control'})
        self.fields['handyman'].widget.attrs.update({'class' : 'form-control ip-form'})
        self.fields['location'].widget = GMapPointWidget(attrs={'map_width': 800, 'map_height': 500})

    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee.amount < 0:
            raise forms.ValidationError(
            self.error_messages['negative_currency'],
            code='negative_currency'
            )

        return fee
