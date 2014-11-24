

from users.models import UserProfile
from .serializers import UserSerializer


from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

class UsersList(APIView):

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data)

class UsersDetail(APIView):

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)