
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from users.models import UserProfile, CITY_SELECTION
from jobs.models import Jobs

from rest_framework import exceptions, serializers

import logging

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'name',
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
        if password1 and password2 and password1 != password2:
            msg = _('Passwords do not match.')
            raise exceptions.ParseError(msg)
        return password2

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
        instance = super(UserSignupSerializer, self).restore_object(attrs, instance)
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
            'destination_home',
            )

class NewJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = (
            'customer',
            'fee',
            'jobtype',
            'remarks',
            'destination_home',
            )

class JobResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = (
            'id',
            'customer',
            'fee',
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