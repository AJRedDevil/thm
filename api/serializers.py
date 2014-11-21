

from users.models import UserProfile

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'first_name',
            'last_name',
            'displayname',
            'is_active',
            'phone',
            )