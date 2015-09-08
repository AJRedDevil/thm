

import logging
import os

from django import forms
from django.utils.translation import ugettext_lazy as _


from .models import Inventory, ToolInventory
from apps.users.models import UserProfile

logger = logging.getLogger(__name__)

class InventoryCreationForm(forms.ModelForm):
    """Form to create the Inventory 
    """
    error_messages = {
        'negative_currency': _("Price can never be negative!"),
        'zero_currency':_("Price cannot have zero value"),
        'complete_job': _("Job once complete cannot be reverted"),
        }

    class Meta:
        model = Inventory
        fields = ['name','image']

    def __init__(self, *args, **kwargs):
        super(InventoryCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={'class': 'form-control'}
        self.fields['image'].widget.attrs = {'class':'form-control'}

    def clean_image(self):
        image = self.cleaned_data['image']

        if type(image) is not bool and image is not None:
            ALLOWED_FILE_EXTS = ['.png', '.jpg', '.jpeg']
            IMAGE_MAX_SIZE = 2097152
            root, ext = os.path.splitext(image.name.lower())
            if ext not in ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. \
                    Allowed file types are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                            'valid_exts_list': valid_exts})
            try:
                if image.size > IMAGE_MAX_SIZE:
                    error = _("Your profile picture is too big (%(size)s), "
                              "the maximum allowed size is %(max_valid_size)s")
                    raise forms.ValidationError(error % {
                        'size': filesizeformat(image.size),
                        'max_valid_size': filesizeformat(IMAGE_MAX_SIZE)
                    })
            except Exception:
                # returned because of a possibility where by the image is
                # removed for some reason either manually or by mistake
                return image

            return image
        return image


class InventoryEditFromAdmin(forms.ModelForm):
    """Form to edit Inventory by admin
    """
    error_messages = {
        'negative_currency': _("Price can never be negative!"),
        'zero_currency':_("Price cannot have zero value"),
        'complete_job': _("Job once complete cannot be reverted"),
        }

    class Meta:
        model = Inventory
        fields = ['name', 'image']

    def __init__(self, *args, **kwargs):
        super(InventoryEditFromAdmin, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'class': 'form-control'}
        self.fields['image'].widget.attrs = {'class':'form-control'}

    def clean_image(self):
        image = self.cleaned_data['image']

        if type(image) is not bool and image is not None:
            ALLOWED_FILE_EXTS = ['.png', '.jpg', '.jpeg']
            IMAGE_MAX_SIZE = 2097152
            root, ext = os.path.splitext(image.name.lower())
            if ext not in ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. \
                    Allowed file types are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                            'valid_exts_list': valid_exts})
            try:
                if image.size > IMAGE_MAX_SIZE:
                    error = _("Your profile picture is too big (%(size)s), "
                              "the maximum allowed size is %(max_valid_size)s")
                    raise forms.ValidationError(error % {
                        'size': filesizeformat(image.size),
                        'max_valid_size': filesizeformat(IMAGE_MAX_SIZE)
                    })
            except Exception:
                # returned because of a possibility where by the image is
                # removed for some reason either manually or by mistake
                return image

            return image
        return image

class ToolDistributionForm(forms.ModelForm):
    """Form to distribute tools to Handyman
    """
    ids = ToolInventory.objects.filter().values('handyman')
    handyman = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type=1, is_active=True).exclude(id__in=ids),
                                              required=True)
    tools = forms.ModelMultipleChoiceField(queryset=Inventory.objects.filter(), required=True)#, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ToolInventory
        fields = ['handyman', 'tools']

    def __init__(self, *args, **kwargs):
        super(ToolDistributionForm, self).__init__(*args, **kwargs)
        self.fields['handyman'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['tools'].widget.attrs = {'class' : 'form-control'}

class ToolDistributionFromAdmin(forms.ModelForm):
    """Form to distribute tools to Handyman
    """
    # ids = ToolInventory.objects.filter().values('handyman')
    handyman = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type=1, is_active=True),
                                              required=True)
    tools = forms.ModelMultipleChoiceField(queryset=Inventory.objects.filter(), required=True)#, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ToolInventory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ToolDistributionFromAdmin, self).__init__(*args, **kwargs)
        self.fields['handyman'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['tools'].widget.attrs = {'class' : 'form-control'}

