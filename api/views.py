

from users.models import UserProfile, UserToken
from users import handler as user_handler

from .serializers import UserSerializer, AuthTokenSerializer, UserSignupSerializer, UserSignupValidationSerializer


from django.http import Http404, HttpResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import logging
import simplejson as json

# Init Logger
logger = logging.getLogger(__name__)

class UsersList(APIView):

    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serialized_users = UserSerializer(users, many=True)
        responsedata = dict(data=serialized_users.data, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

class UsersDetail(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serialized_user = UserSerializer(user)
        responsedata = dict(data=serialized_user.data, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

class UserSignup(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        """
        Lets a user signup 
        """
        data = request.DATA
        data['address'] = json.dumps(dict(city=data['city'], streetaddress=data['streetaddress']))
        serialized_user = UserSignupValidationSerializer(data=request.DATA)
        if serialized_user.is_valid():
            serialized_user = UserSignupSerializer(data=request.DATA)
            if serialized_user.is_valid():
                user = serialized_user.save()
                UserToken.objects.create(user=user)
                um = user_handler.UserManager()
                msgstatus = um.sendVerfTextApp(user.id)
                logging.warn(msgstatus)
                logging.warn("user {0} is created".format(user.phone))
                token = Token.objects.get(user=user)
                responsedata = dict (token=token.key, status=status.HTTP_201_CREATED, success=True)
                return HttpResponse(json.dumps(responsedata), content_type="application/json")
        return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = Token.objects.get_or_create(user=user)
            return HttpResponse(json.dumps({'token': token.key, 'success' : True}), content_type="application/json")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(json.dumps({'status':status.HTTP_400_BAD_REQUEST, 'success':False}), content_type="application/json")


obtain_auth_token = ObtainAuthToken.as_view()