
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from users.models import UserProfile, CITY_SELECTION

from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.formfields import PhoneNumberField
from rest_framework import exceptions, serializers

import logging
import jsonfield

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'name',
            'is_active',
            'phone',
            )

class UserSignupSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    city = serializers.ChoiceField(choices=CITY_SELECTION)
    streetaddress = serializers.CharField()
    address = jsonfield.JSONField()

    class Meta:
        model = UserProfile
        fields = (
            'name',
            'phone',
            'address',
            )

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