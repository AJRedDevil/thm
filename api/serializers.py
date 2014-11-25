
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from users.models import UserProfile, CITY_SELECTION

from rest_framework import exceptions, serializers

import logging

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'name',
            'is_active',
            'phone',
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
    password2 = serializers.CharField()

    class Meta:
        model = UserProfile
        fields = (
            'name',
            'phone',
            'address',
            'password2',
            'current_address'
            )

    def restore_object(self, attrs, instance=None):
        instance = super(UserSignupSerializer, self).restore_object(attrs, instance)
        logging.warn(attrs)
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