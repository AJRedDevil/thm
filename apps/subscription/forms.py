

import logging

from django import forms
from djmoney.models.fields import MoneyField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .models import SubscriptionPackage, Subscriber, Subscription
from apps.users.models import UserProfile

logger = logging.getLogger(__name__)

class SubscriptionPackageCreationForm(forms.ModelForm):
    """Form to create SubscriptionPackage
    """
    error_messages = {
        'negative_currency': _("Price can never be negative!"),
        'zero_currency':_("Price cannot have zero value"),
    }

    class Meta:
        model = SubscriptionPackage
        fields = ['name', 'price', 'max_repair', 'discount']

    def __init__(self, *args, **kwargs):
        super(SubscriptionPackageCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={'class': 'form-control'}
        self.fields['price'].widget.attrs={'class': 'form-control'}
        self.fields['max_repair'].widget.attrs={'class': 'form-control'}
        self.fields['discount'].widget.attrs={'class': 'form-control'}

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price.amount < 0:
            raise forms.ValidationError(
            self.error_messages['negative_currency'],
            code='negative_currency'
            )

        return price

class SubscriptionPackageEditForm(forms.ModelForm):
    """Form to edit SubscriptionPackage
    """
    error_messages = {
        'negative_currency': _("Price can never be negative!"),
        'zero_currency':_("Price cannot have zero value"),
    }

    class Meta:
        model = SubscriptionPackage
        fields = ['name', 'price', 'max_repair', 'discount']

    def __init__(self, *args, **kwargs):
        super(SubscriptionPackageEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs={'class': 'form-control'}
        self.fields['price'].widget.attrs={'class': 'form-control'}
        self.fields['max_repair'].widget.attrs={'class': 'form-control'}
        self.fields['discount'].widget.attrs={'class': 'form-control'}

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price.amount < 0:
            raise forms.ValidationError(
            self.error_messages['negative_currency'],
            code='negative_currency'
            )

        return price

class SubscriberCreationForm(forms.ModelForm):
    """Form to create subscriber
    """
    primary_contact_person = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type=2, is_active=True), required=True)
    secondary_contact_person = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type=2, is_active=True), required=True)

    class Meta:
        model = Subscriber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubscriberCreationForm, self).__init__(*args, **kwargs)
        self.fields['primary_contact_person'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['secondary_contact_person'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['subscriber_name'].widget.attrs={'class': 'form-control'}
        self.fields['office_number'].widget.attrs={'class': 'form-control'}
        self.fields['is_office'].widget.attrs={'class': 'form-control'}

class SubscriberEditForm(forms.ModelForm):
    """Form to edit subscriber
    """
    primary_contact_person = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type=2, is_active=True), required=True)
    secondary_contact_person = forms.ModelChoiceField(queryset=UserProfile.objects.filter(user_type=2, is_active=True), required=True)

    class Meta:
        model = Subscriber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SubscriberEditForm, self).__init__(*args, **kwargs)
        self.fields['primary_contact_person'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['secondary_contact_person'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['subscriber_name'].widget.attrs={'class': 'form-control'}
        self.fields['office_number'].widget.attrs={'class': 'form-control'}
        self.fields['is_office'].widget.attrs={'class': 'form-control'}

class SubscriptionCreationForm(forms.ModelForm):
    """Form to create subscription to package
    """
    error_messages = {
        'non_terminated': _("Current Subscription should be termiated before createing another subscription"),
        'month_long': _("Subscription should be atleast a month long"),
        'empty_package': _("Subscription should have a package associated with it"),
        'empty_subscriber': _("Oops you forgot the subscriber!!"),
    }

    package = forms.ModelChoiceField(queryset=SubscriptionPackage.objects.all(), required=False)
    subscriber = forms.ModelChoiceField(queryset=Subscriber.objects.filter(is_office=True), required=False)
    
    class Meta:
        model = Subscription
        fields = ['start_date', 'end_date', 'package', 'subscriber']

    def __init__(self, *args, **kwargs):
        super(SubscriptionCreationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs={'class': 'form-control datePicker'}
        self.fields['end_date'].widget.attrs={'class': 'form-control datePicker'}
        self.fields['package'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['subscriber'].widget.attrs={'class': 'form-control ip-form'}

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        gap = end_date - start_date
        if gap.days < 30:
            raise forms.ValidationError(
            self.error_messages['month_long'],
            code='month_long'
            )
        return end_date

    def clean_subscriber(self):
        subscriber = self.cleaned_data.get('subscriber')
        if not subscriber:
            raise forms.ValidationError(
            self.error_messages['empty_subscriber'],
            code='empty_subscriber'
            )

        current_active_subsciption = Subscription.objects.filter(subscriber=subscriber, terminated=False)
        if current_active_subsciption:
            raise forms.ValidationError(
            self.error_messages['non_terminated'],
            code='non_terminated'
            )

        return subscriber

    def clean_package(self):
        package = self.cleaned_data.get("package")
        if not package:
            raise forms.ValidationError(
            self.error_messages['empty_package'],
            code='empty_package'
            )
        return package


class SubscriptionEditForm(forms.ModelForm):
    """Form to edit subscription to package
    """
    package = forms.ModelChoiceField(queryset=SubscriptionPackage.objects.filter(), required=False)
    
    class Meta:
        model = Subscription
        fields = ['start_date','end_date', 'package', 'terminated']

    def __init__(self, *args, **kwargs):
        super(SubscriptionEditForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs={'class': 'form-control datePicker'}
        self.fields['end_date'].widget.attrs={'class': 'form-control datePicker'}
        self.fields['package'].widget.attrs={'class': 'form-control ip-form'}
        self.fields['terminated'].widget.attrs={'class': 'form-control'}

