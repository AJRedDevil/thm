

from users.models import UserProfile, UserToken
from jobs.models import Jobs
from users import handler as user_handler

import serializers

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

# class UsersList(APIView):

#     def get(self, request, format=None):
#         users = UserProfile.objects.all()
#         serialized_users = serializers.UserSerializer(users, many=True)
#         responsedata = dict(data=serialized_users.data, success=True)
#         return HttpResponse(json.dumps(responsedata),content_type="application/json")

class UsersDetail(APIView):
    """
    Userdetail resource
    """

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        """
        Returns detail of a user
        ---
        response_serializer: serializers.UserSerializer
        """
        user = self.get_object(pk)
        serialized_user = serializers.UserSerializer(user)
        responsedata = dict(data=serialized_user.data, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

class UserSignup(APIView):
    """
    User signup resource
    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        """
        Allows a user to signup
        ---
        request_serializer: serializers.UserSignupValidationSerializer
        response_serializer: serializers.SignupResponseSerializer
        """
        data = request.DATA.copy()
        data['address'] = json.dumps(dict(city=data['city'], streetaddress=data['streetaddress']))
        serialized_user = serializers.UserSignupValidationSerializer(data=data)
        if serialized_user.is_valid():
            serialized_user = serializers.UserSignupSerializer(data=data)
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
    """
    User login resource
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = serializers.AuthTokenSerializer
    model = Token

    def post(self, request):
        """
        Allows a user to login 
        ---
        request_serializer: serializers.AuthTokenSerializer
        response_serializer: serializers.SigninResponseSerializer
        """
        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid():
            user = serializer.object['user']
            token, created = Token.objects.get_or_create(user=user)
            return HttpResponse(json.dumps({'token': token.key, 'success' : True}), content_type="application/json")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(json.dumps({'status':status.HTTP_400_BAD_REQUEST, 'success':False}), content_type="application/json")

obtain_auth_token = ObtainAuthToken.as_view()

class JobDetail(APIView):
    """
    Jobdetail resource
    """

    def get_object(self, pk):
        try:
            return Jobs.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        """
        Returns detail of a job
        ---
        response_serializer: serializers.JobResponseSerializer
        """
        job = self.get_object(pk)
        serialized_user = serializers.JobResponseSerializer(job)
        data = serialized_user.data
        data['creation_date'] = str(data['creation_date'])
        data['completion_date'] = str(data['completion_date'])
        responsedata = dict(data=data, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

class JobsDetail(APIView):
    """
    New Job resource
    """
    def get(self, request, format=None):
        jobs = Jobs.objects.all()
        serialized_jobs = serializers.JobResponseSerializer(jobs, many=True)
        data = serialized_jobs.data
        for datum in data:
            datum['creation_date'] = str(datum['creation_date'])
            datum['completion_date'] = str(datum['completion_date'])
        responsedata = dict(data=data, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

    def post(self, request, format=None):
        """
        Allows a user to create a job
        ---
        request_serializer: serializers.JobSerializer
        response_serializer: serializers.JobAPIResponseSerializer
        """
        user = request.user
        data = request.DATA.copy()
        serialized_job = serializers.JobSerializer(data=data)
        if serialized_job.is_valid():
            data['customer'] = user.id
            data['fee'] = "5.99"
            serialized_job = serializers.NewJobSerializer(data=data)
            if serialized_job.is_valid():
                job = serialized_job.save()
                logging.warn("job {0} is created".format(job.id))
                responsedata = dict (status=status.HTTP_201_CREATED, success=True)
                return HttpResponse(json.dumps(responsedata), content_type="application/json")
        return Response(serialized_job.errors, status=status.HTTP_400_BAD_REQUEST)

