
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from apps.users.models import UserProfile, CITY_SELECTION
from jobs.models import Jobs

from rest_framework import exceptions, serializers
from phonenumber_field.phonenumber import PhoneNumber as intlphone

import apps.users.handler as user_handler

import logging
# Init Logger
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'name',
            'user_type',
            'profile_image',
            'phone_status',
        )


class UserSignupValidationSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    city = serializers.ChoiceField(choices=CITY_SELECTION)
    streetaddress = serializers.CharField()
    current_address = serializers.CharField(required=False)

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        phone_number = attrs.get('phone')

        # Password length validation
        if password1 and password2:
            if len(password1) < 6 or len(password2) < 6:
                msg = _('Password must be more than 6 chars.')
                raise exceptions.ParseError(msg)

        # Password match validation
        if password1 and password2 and password1 != password2:
            msg = _('Passwords do not match.')
            raise exceptions.ParseError(msg)

        # Phone number validation
        phone = intlphone.from_string(phone_number)
        if str(phone.country_code) != '977':
            msg = _("Your country is not supported as of now!")
            raise exceptions.ParseError(msg)

        # GSM system code for nepal is 98 as per national number plan from NTA
        # That means all the mobile number in nepal must start from 98
        GSM_Code = int(str(phone.national_number)[:2])
        valid_GSM_Code = (96, 97, 98)

        if GSM_Code not in valid_GSM_Code:
            msg = _("Please enter a valid mobile number!"),
            raise exceptions.ParseError(msg)

        return attrs


class UserSignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = (
            'name',
            'phone',
            'address',
            'password1',
            'password2',
            'current_address'
        )

    def restore_object(self, attrs, instance=None):
        instance = super(UserSignupSerializer, self).restore_object(
            attrs, instance)
        instance.set_password(attrs['password2'])
        return instance


class AuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            user = authenticate(username=phone, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise exceptions.PermissionDenied(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.AuthenticationFailed(msg)
        else:
            msg = _('Must include "phone" and "password"')
            raise exceptions.ParseError(msg)

        attrs['user'] = user
        return attrs


class SigninResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    success = serializers.BooleanField()


class SignupResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    success = serializers.BooleanField()
    status = serializers.IntegerField()


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = (
            'jobtype',
            'remarks',
        )


class NewJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = (
            'customer',
            'jobtype',
            'remarks',
        )


class JobResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = (
            'status',
            'creation_date',
            'completion_date',
            'jobtype',
            'remarks',
        )


class JobAPIResponseSerializer(serializers.Serializer):
    """
    Response Serializer for requests over in API
    """
    success = serializers.BooleanField()
    status = serializers.IntegerField()


class PhoneVerifySerializer(serializers.Serializer):
    """
    Response Serializer for requests over in API
    """
    verf_code = serializers.CharField()

    def validate(self, attrs):
        um = user_handler.UserManager()
        verf_code = attrs.get('verf_code')
        request = self.context.get('request', None)

        if verf_code:
            if request.user.phone_status is True:
                msg = _('Phone already verified!')
                raise exceptions.PermissionDenied(msg)

            if not um.checkVerfCode(request.user, verf_code):
                msg = _('Provided code is incorrect!')
                raise exceptions.PermissionDenied(msg)
