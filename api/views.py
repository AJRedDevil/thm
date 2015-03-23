

from users.models import UserProfile, UserToken
from jobs.models import Jobs
from users import handler as user_handler

import serializers

from django.http import Http404, HttpResponse

from ipware.ip import get_real_ip, get_ip
from libs.sparrow_handler import Sparrow

from rest_framework.views import APIView
from rest_framework import status
from rest_framework import parsers
from rest_framework import renderers
from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from phonenumber_field.phonenumber import PhoneNumber as intlphone

import logging
import simplejson as json

# Init Logger
logger = logging.getLogger(__name__)

# # Below shoudl be commented out because
# # we do not return list of all users
# class UsersList(APIView):

#     def get(self, request, format=None):
#         users = UserProfile.objects.all()
#         serialized_users = serializers.UserSerializer(users, many=True)
#         responsedata = dict(detail=serialized_users.data, success=True)
#         return HttpResponse(
#             json.dumps(responsedata),
#             content_type="application/json",
#             status=status.HTTP_200_OK)


class UsersDetail(APIView):
    """
    Userdetail resource
    """

    def get_object(self, pk):
        try:
            return UserProfile.objects.get(userref=pk)
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
        responsedata = dict(detail=serialized_user.data, success=True)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json",
            status=status.HTTP_200_OK)


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
        user = request.user
        ## Error if user is already authenticated
        if user.is_authenticated():
            responsedata = dict(success=False)
            return HttpResponse(
                json.dumps(responsedata),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST)

        # Creating an mutable dict from the request.DATA
        # so we can add address details to it
        data = request.DATA.copy()
        ## Creating a address object
        serialized_user = serializers.UserSignupValidationSerializer(data=data)
        if serialized_user.is_valid():
            data['address'] = json.dumps(dict(
                city=data['city'],
                streetaddress=data['streetaddress']))
            serialized_user = serializers.UserSignupSerializer(data=data)
            if serialized_user.is_valid():
                user = serialized_user.save()
                # Creating a user transaction token for the user
                UserToken.objects.create(user=user)
                # Using User handler to send out verification
                # code to the user on the phone
                um = user_handler.UserManager()
                msgstatus = um.sendVerfTextApp(user.id)
                logging.warn(msgstatus)
                logging.warn("user {0} is created from app".format(user.phone))
                # Creating a auth token for the user
                # and return the same as response
                token = Token.objects.get(user=user)
                tokendata = dict(token=token.key)
                responsedata = dict(detail=tokendata, success=True)
                return HttpResponse(
                    json.dumps(responsedata),
                    content_type="application/json",
                    status=status.HTTP_201_CREATED)
        responsedata = dict(detail=serialized_user.errors)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(APIView):
    """
    User login resource
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,)
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
            tokendata = dict(token=token.key)
            responsedata = dict(detail=tokendata, success=True)
            return HttpResponse(
                json.dumps(responsedata),
                content_type="application/json")
        responsedata = dict(detail=serializer.errors, success=False)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthToken.as_view()


class JobDetail(APIView):
    """
    Jobdetail resource
    """

    def get_object(self, pk, user):
        try:
            ## For staffs show all
            if user.user_type==0:
                return Jobs.objects.get(jobref=pk)
            ## For handymen, show data only if they were assigned to it
            elif user.user_type==1:
                return Jobs.objects.get(jobref=pk, handyman_id=user.id)
            ## For Customers, show data only if they created it
            elif user.user_type==2:
                return Jobs.objects.get(jobref=pk, customer_id=user.id)
            else:
                raise Http404
        except Jobs.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        """
        Returns detail of a job
        ---
        response_serializer: serializers.JobResponseSerializer
        """
        user = request.user
        job = self.get_object(pk, user)
        serialized_user = serializers.JobResponseSerializer(job)
        data = serialized_user.data
        data['creation_date'] = str(data['creation_date'])
        data['completion_date'] = str(data['completion_date'])
        responsedata = dict(data=data, status=status.HTTP_200_OK, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

class JobsDetail(APIView):
    """
    New Job resource
    """
    def get(self, request, format=None):
        user = request.user
        if request.GET:
            jobstatus = request.GET['jobstatus']
            logging.warn(jobstatus)
            logging.warn(user.user_type)
            ## If THM Staffs retrieve all
            if user.user_type == 0:
                jobs = Jobs.objects.filter(status=jobstatus)
                logging.warn(jobs)
            ## If it's a handymen, only show requests which they were assigned to
            elif user.user_type == 1:
                jobs = Jobs.objects.filter(handyman_id=user.id, status=jobstatus)
            ## If it's a customer only show requests that they created
            elif user.user_type == 2:
                jobs = Jobs.objects.filter(customer_id=user.id, status=jobstatus)
            else:
                responsedata = dict(status=status.HTTP_400_BAD_REQUEST, success=False)
                return HttpResponse(json.dumps(responsedata), content_type="application/json")
        else:
            if user.user_type == 0:
                jobs = Jobs.objects.filter()
            ## If it's a handymen, only show requests which they were assigned to
            elif user.user_type == 1:
                jobs = Jobs.objects.filter(handyman_id=user.id)
            ## If it's a customer only show requests that they created
            elif user.user_type == 2:
                jobs = Jobs.objects.filter(customer_id=user.id)
            else:
                responsedata = dict(status=status.HTTP_400_BAD_REQUEST, success=False)
                return HttpResponse(json.dumps(responsedata), content_type="application/json")

        serialized_jobs = serializers.JobResponseSerializer(jobs, many=True)
        data = serialized_jobs.data
        for datum in data:
            datum['creation_date'] = str(datum['creation_date'])
            datum['completion_date'] = str(datum['completion_date'])
        responsedata = dict(data=data, status=status.HTTP_200_OK, success=True)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")

    def post(self, request, format=None):
        """
        Allows a user to create a job
        ---
        request_serializer: serializers.JobSerializer
        response_serializer: serializers.JobAPIResponseSerializer
        """
        user = request.user
        ## We only allow a customer or THM staffs to create job requests
        if user.user_type == 1:
            responsedata = dict(status=status.HTTP_400_BAD_REQUEST, success=False)
            return HttpResponse(json.dumps(responsedata), content_type="application/json")
        data = request.DATA.copy()
        serialized_job = serializers.JobSerializer(data=data)
        if serialized_job.is_valid():
            data['customer'] = user.id
            serialized_job = serializers.NewJobSerializer(data=data)
            if serialized_job.is_valid():
                job = serialized_job.save()
                if job.jobtype == 1:
                    vas = Sparrow()
                    msg = "Request for a plumber received and is queued for processing, a plumber would be put in touch with you soon!"
                    msgstatus = vas.sendDirectMessage(msg, user.phone)
                    adminmsg = "Request for a plumber received from {0}".format(user.phone.as_national)
                    adminmsgstatus = vas.sendDirectMessage(adminmsg, intlphone.from_string('+9779802036633'))
                    logger.warn(msgstatus)
                    logger.warn(adminmsgstatus)
                if job.jobtype == 2:
                    vas = Sparrow()
                    msg = "Request for an electrician received and is queued for processing, an electrician would be put in touch with you soon!"
                    msgstatus = vas.sendDirectMessage(msg, user.phone)
                    adminmsg = "Request for an electrician received from {0}".format(user.phone.as_national)
                    adminmsgstatus = vas.sendDirectMessage(adminmsg, intlphone.from_string('+9779802036633'))
                    logger.warn(msgstatus)
                    logger.warn(adminmsgstatus)
                logging.warn("job {0} is created".format(job.id))
                responsedata = dict (status=status.HTTP_201_CREATED, success=True)
                return HttpResponse(json.dumps(responsedata), content_type="application/json")
        responsedata=dict(data=serialized_job.errors, status=status.HTTP_400_BAD_REQUEST, success=False)
        return HttpResponse(json.dumps(responsedata),content_type="application/json")


class VerifyPhone(APIView):
    """
    Phone verification resource
    """

    def get(self, request, format=None):
        """
        Sends the user a text message containig the verification code
        """
        user = request.user
        client_internal_ip = get_real_ip(request)
        client_public_ip = get_ip(request)
        if user.phone_status is False:
            um = user_handler.UserManager()
            UserToken.objects.create(user=user)
            ### Update User Events
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(
                client_public_ip=client_public_ip,
                client_internal_ip=client_internal_ip)
            eventhandler.setevent(request.user, 3, extrainfo)
            ### Send user a SMS stating that his phone has been verified
            um.sendVerfTextApp(user.id)
            logger.debug("Verification code sent to the {0}".format(user.phone))
            responsedata = dict(success=True)
            return HttpResponse(
                json.dumps(responsedata),
                content_type="application/json")
        responsedata = dict(detail="Phone already verified", success=False)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST,)

    def post(self, request):
        """
        Allows a user to verify his phone
        ---
        request_serializer: serializers.PhoneVerifySerializer
        response_serializer: serializers.JobAPIResponseSerializer
        """
        serializer = serializers.PhoneVerifySerializer(
            data=request.POST, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.phone_status = True
            user.save()
            responsedata = dict(success=True)
            return HttpResponse(
                json.dumps(responsedata),
                content_type="application/json")
        responsedata = dict(detail=serializer.errors, success=False)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json",
            status=status.HTTP_400_BAD_REQUEST,)


class CheckPhoneStatus(APIView):
    """
    Phone status resource
    """

    def get(self, request, format=None):
        """
        Returns the status of the phone verification
        """
        user = request.user
        responsedata = dict(success=user.phone_status)
        return HttpResponse(
            json.dumps(responsedata),
            content_type="application/json")
