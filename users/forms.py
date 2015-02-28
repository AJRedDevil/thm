
from collections import OrderedDict

from django import forms
from django.conf import settings

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat

from .models import UserProfile, CITY_SELECTION, EarlyBirdUser
import handler as user_handler

import os
from phonenumber_field.formfields import PhoneNumberField
import logging
logger = logging.getLogger(__name__)


class VerifyPhoneForm(forms.Form):
    """
    A form that takes phone number as the data
    """
    error_messages = {
        'wrong_code': _("Provided code is not correct!"),
    }

    verf_code = forms.CharField(
        label=_("verf_code"),
        widget=forms.TextInput, min_length=6,
        error_messages={
        'required' : 'Please provide with the verification code sent on your mobile !',
        }
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(VerifyPhoneForm, self).__init__(*args, **kwargs)

    def clean_verf_code(self):
        um = user_handler.UserManager()
        verf_code = self.cleaned_data.get("verf_code")
        user = self.request.user
        if not um.checkVerfCode(user, verf_code):
            raise forms.ValidationError(
                self.error_messages['wrong_code'],
                code='wrong_code',
            )
        return verf_code


class EBUserPhoneNumberForm(forms.ModelForm):
    """
    A form that takes phone number as the data
    """
    phone = PhoneNumberField()

    error_messages = {
        'country_notsupported': _("Your country is not supported as of now!"),
        'duplicate_phone': _("You have already registered!"),
        'mobile_phone': _("Please enter a valid mobile number!"),
    }

    class Meta:
        model = EarlyBirdUser
        fields = ['phone']

    def clean_phone(self):

        phone = self.cleaned_data.get("phone")
        signedupusers = EarlyBirdUser.objects.all()
        if str(phone.country_code) != '977':
            raise forms.ValidationError(
                self.error_messages['country_notsupported'],
                code='country_notsupported',
            )

        # GSM system code for nepal is 98 as per national number plan from NTA
        # That means all the mobile number in nepal must start from 98
        GSM_Code = int(str(phone.national_number)[:2])
        valid_GSM_Code = (96, 97, 98)

        if GSM_Code not in valid_GSM_Code:
            raise forms.ValidationError(
                self.error_messages['mobile_phone'],
                code='mobile_phone',
            )

        if phone in signedupusers:
            raise forms.ValidationError(
                self.error_messages['duplicate_phone'],
                code='duplicate_phone',
            )
        return phone

    def save(self, commit=True):
        data = super(EBUserPhoneNumberForm, self).save(commit=False)
        if commit:
            data.save()
        return data

# class HMUserPhoneNumberForm(forms.ModelForm):
#     """
#     A form that takes phone number as the data
#     """
#     phone = PhoneNumberField()

#     error_messages = {
#         'country_notsupported': _("Your country is not supported right now!"),
#         }

#     class Meta:
#         model = EarlyBirdHandymen
#         fields = ['phone']

#     def clean_phone(self):
#         phone = self.cleaned_data.get("phone")
#         if str(phone.country_code) != '977':
#             raise forms.ValidationError(
#                 self.error_messages['country_notsupported'],
#                 code='country_notsupported',
#             )
#         return phone

#     def save(self, commit=True):
#         data = super(HMUserPhoneNumberForm, self).save(commit=False)
#         if commit:
#             data.save()
#         return data


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, from the given data,
    this runs when the user uses the signup form
    """
    phone = forms.ModelChoiceField(
        EarlyBirdUser.objects.filter(confirmed=False).order_by('id'))
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput, min_length=6,
        error_messages={
            'required': 'Please provide with a password !',
            'min_length': 'The password has to be more than 6 characters !',
        })
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput, min_length=6,
        help_text=_("Enter the same password as above, for verification."),
        error_messages={
            'required': 'Please provide with a password confirmation !',
            'min_length': 'The password has to be more than 6 characters !',
        })
    city = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        })

    streetaddress = forms.CharField(
        error_messages={
            'required': 'Street Address is required !',
        })

    error_messages = {
        'password_mismatch': _("The two password fields didn't match. \
            Please re-verify your passwords !"),
        'country_notsupported': _("Your country is not supported right now!"),
    }

    class Meta:
        model = UserProfile
        fields = ['name', 'phone']

    def __init__(self, *args, **kwargs):
        if 'ebuser' in kwargs:
            ebuser = kwargs.pop('ebuser')
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if ebuser is not None:
            ebusers = EarlyBirdUser.objects.filter(
                confirmed=False,
                phone=ebuser).order_by('id')
            self.fields['phone'].choices = [(h.pk, h.phone) for h in ebusers]
        self.fields['name'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Hari Sharma'
        }
        self.fields['phone'].widget.attrs = {'class': 'form-control'}
        self.fields['password1'].widget.attrs = {'class': 'form-control'}
        self.fields['password2'].widget.attrs = {'class': 'form-control'}
        self.fields['city'].widget.attrs = {'class': 'form-control'}
        self.fields['streetaddress'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ganeshthan, Kamaladi'
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_phone(self):
        # self.cleaned_data.get("phone") is a User object
        phone = self.cleaned_data.get("phone").phone
        if str(phone.country_code) != '977':
            raise forms.ValidationError(
                self.error_messages['country_notsupported'],
                code='country_notsupported',
            )
        return phone

    # def clean_email(self):
    #     # Since User.username is unique, this check is redundant,
    #     # but it sets a nicer error message than the ORM. See #13147.
    #     email = self.cleaned_data["email"]
    #     try:
    #         UserProfile._default_manager.get(email=email)
    #     except UserProfile.DoesNotExist:
    #         return email
    #     raise forms.ValidationError(
    #         self.error_messages['duplicate_email'],
    #         code='duplicate_email',
    #     )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.avatar_file_name=settings.STATIC_URL+'img/default.png'
        if commit:
            user.save()
        return user


class UserSignupForm(forms.ModelForm):
    """
    A form for user signups
    """
    phone = PhoneNumberField()
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
        min_length=6,
        error_messages={
            'required': 'Please provide with a password !',
            'min_length': 'The password has to be more than 6 characters !',
        })
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput, min_length=6,
        help_text=_("Enter the same password as above, for verification."),
        error_messages={
            'required': 'Please provide with a password confirmation !',
            'min_length': 'The password has to be more than 6 characters !',
        })
    city = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        })

    streetaddress = forms.CharField(
        error_messages={
            'required': _('Street/Apt. Address where the shipment is to be \
            picked up from is required !'),
        })

    error_messages = {
        'password_mismatch': _("The two password fields didn't match. \
            Please re-verify your passwords !"),
        'country_notsupported': _("Your country is not supported right now!"),
    }

    class Meta:
        model = UserProfile
        fields = ['name', 'phone']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_phone(self):

        phone = self.cleaned_data.get("phone")
        if str(phone.country_code) != '977':
            raise forms.ValidationError(
                self.error_messages['country_notsupported'],
                code='country_notsupported',
            )

        # GSM system code for nepal is 98 as per national number plan from NTA
        # That means all the mobile number in nepal must start from 98
        GSM_Code = int(str(phone.national_number)[:2])
        valid_GSM_Code = (96, 97, 98)

        if GSM_Code not in valid_GSM_Code:
            raise forms.ValidationError(
                self.error_messages['mobile_phone'],
                code='mobile_phone',
            )

        return phone

    # def clean_email(self):
    #     # Since User.username is unique, this check is redundant,
    #     # but it sets a nicer error message than the ORM. See #13147.
    #     email = self.cleaned_data["email"]
    #     try:
    #         UserProfile._default_manager.get(email=email)
    #     except UserProfile.DoesNotExist:
    #         return email
    #     raise forms.ValidationError(
    #         self.error_messages['duplicate_email'],
    #         code='duplicate_email',
    #     )

    def save(self, commit=True):
        user = super(UserSignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.avatar_file_name=settings.STATIC_URL+'img/default.png'
        if commit:
            user.save()
        return user


class LocalAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    phone = PhoneNumberField()
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct phone number and password. "
                           "Note that password may be case-sensitive."),
        'inactive': _("This account is inactive, \
            please contact us at info@thehomerepairapp.com ! "),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LocalAuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "phone" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(
            UserModel.USERNAME_FIELD)
        # if self.fields['username'].label is None:
        #     self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')

        if phone and password:
            self.user_cache = authenticate(username=phone,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class HMUserChangeForm(UserChangeForm):
    """
    Form to edit user details,
    this only changes the general details of the user and not the password
    """
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for fieldname in ['username']:
            del self.fields['password']
            del self.fields['username']

    city = forms.ChoiceField(
        choices=CITY_SELECTION,
        error_messages={
            'required': 'Name of the city is required !',
            'invalid_choice': 'Please select one of the options available !'
        }
    )

    streetaddress = forms.CharField(
        error_messages={'required': 'Street Address is required !', }
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Hari Wagle'}),
            'phone': forms.TextInput(attrs={'placeholder': '9802036633'}),
        }
        error_messages = {
            'name': {
                'required': 'Your name is required!',
            },
            'phone': {
                'required': 'Please provide with a valid phone address!',
            },
        }

    def save(self, commit=True):
        user = super(HMUserChangeForm, self).save(commit=False)
        return user



# class SetPasswordForm(forms.Form):
#     """
#     A form that lets a user change set his/her password without entering the
#     old password
#     """
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#         'password1' : {
#             'required' : 'Please provide with a password !',
#         },
#         'password2' : {
#             'required' : 'Please provide with a password confirmation !',
#         },
#     }
#     new_password1 = forms.CharField(label=_("New password"),
#                                     widget=forms.PasswordInput)
#     new_password2 = forms.CharField(label=_("New password confirmation"),
#                                     widget=forms.PasswordInput)

#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)

#     def clean_new_password2(self):
#         password1 = self.cleaned_data.get('new_password1')
#         password2 = self.cleaned_data.get('new_password2')
#         if password1 and password2:
#             if password1 != password2:
#                 raise forms.ValidationError(
#                     self.error_messages['password_mismatch'],
#                     code='password_mismatch',
#                 )
#         return password2

#     def save(self, commit=True):
#         self.user.set_password(self.cleaned_data['new_password1'])
#         if commit:
#             self.user.save()
#         return self.user


# class PasswordChangeForm(SetPasswordForm):
#     """
#     A form that lets a user change his/her password by entering
#     their old password.
#     """
#     error_messages = dict(SetPasswordForm.error_messages, **{
#         'password_incorrect': _("Your old password was entered incorrectly. "
#                                 "Please enter it again."),
#     })
#     old_password = forms.CharField(label=_("Old password"),
#                                    widget=forms.PasswordInput)

#     def clean_old_password(self):
#         """
#         Validates that the old_password field is correct.
#         """
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise forms.ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password

# PasswordChangeForm.base_fields = OrderedDict(
#     (k, PasswordChangeForm.base_fields[k])
#     for k in ['old_password', 'new_password1', 'new_password2']
# )
