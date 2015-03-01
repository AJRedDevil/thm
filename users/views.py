

#All Djang Imports
# from django.conf import settings
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
# from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, Http404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

#All local imports (libs, contribs, models)
import handler as user_handler
from phonenumber_field.phonenumber import PhoneNumber as intlphone
from thm.decorators import is_superuser
from .models import UserProfile, EarlyBirdUser, UserToken
from .forms import UserCreationForm, UserSignupForm, LocalAuthenticationForm, \
    EBUserPhoneNumberForm, VerifyPhoneForm, HMUserChangeForm

#All external imports (libs, packages)
from libs.sparrow_handler import Sparrow
import jobs.handler as jobs_handler
from libs import email_handler
from libs import out_sms as messages
from ipware.ip import get_real_ip, get_ip
import simplejson as json
import logging
import urllib
import requests
import os


# Init Logger
logger = logging.getLogger(__name__)


# Create your views here.
def logout(request):
    """Logs out the user"""
    user = request.user
    if user.is_authenticated():
        eventhandler = user_handler.UserEventManager()
        extrainfo = dict()
        eventhandler.setevent(user, 0, extrainfo)
        logger.debug("{0} logged out".format(request.user))
        auth_logout(request)
    return redirect('index')


def signin(request):
    """
    View to login to the portal
    """
    ## if authenticated redirect to user's homepage directly ##
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    # if request.GET:
    #     next = request.GET['next']

    if request.user.is_authenticated():
        return redirect('home')

    if request.method == "POST":
        auth_form = LocalAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(
                client_public_ip=client_public_ip,
                client_internal_ip=client_internal_ip
            )
            eventhandler.setevent(request.user, 1, extrainfo)
            #Notify the user of his status if he's unavailable
            if request.user.is_authenticated():
                    if request.POST.get('next'):
                        return HttpResponseRedirect(request.POST.get('next'))
                    return redirect('home')
            return redirect('home')

        if auth_form.errors:
            logger.debug("Login Form has errors, %s ", auth_form.errors)

    return redirect('index')
    # return render(request, 'signin.html', locals())


def signup(request):
    """
    Lets a user signup
    """
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    user = request.user
    if user.is_authenticated():
        # redirect user to home if he is already authenticated
        return redirect('home')

    if request.method == "POST":
        request_dict = request.POST.copy()
        phone = request_dict.get('phone')
        if phone == '':
            return redirect('signup')
        try:
            phone = intlphone.from_string(
                request_dict.get('phone'),
                region='NP')
        except Exception as e:
            return redirect('signup')

        user_form = UserSignupForm(request.POST)
        if user_form.is_valid():
            userdata = user_form.save(commit=False)
            userdata.address = dict(
                city=user_form.cleaned_data['city'],
                streetaddress=user_form.cleaned_data['streetaddress'])
            userdata.save()
            authenticate(username=userdata.phone, password=userdata.password)
            userdata.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            UserToken.objects.create(user=userdata)
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(
                client_public_ip=client_public_ip,
                client_internal_ip=client_internal_ip
            )
            eventhandler.setevent(request.user, 1, extrainfo)
            um = user_handler.UserManager()
            um.sendVerfText(userdata.id)
            logger.debug("user created")
            logger.debug("User Details : \n {0}".format(
                serializers.serialize('json', [userdata, ])
            ))
            return redirect('home')
        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
            return render(request, 'signup.html', locals())

    user_form = UserSignupForm
    return render(request, 'signup.html', locals())


@login_required
def verifyPhone(request):
    """
    Lets a user verify his phone number
    """
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    user = request.user
    if user.phone_status is True:
        return redirect('home')

    if request.method == "POST":
        user_form = VerifyPhoneForm(request.POST, request=request)
        if user_form.is_valid():
            um = user_handler.UserManager()
            user = request.user
            ### Update phone status for user
            userdata = um.getUserDetails(user.id)
            userdata.phone_status = True
            userdata.save()
            ### Update User Events
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(
                client_public_ip=client_public_ip,
                client_internal_ip=client_internal_ip
            )
            eventhandler.setevent(request.user, 2, extrainfo)
            ### Send user a SMS stating that his phone has been verified
            um.sendPhoneVerfText(user.id)
            logger.debug("User's phone verified")
            logger.debug("User Details : \n {0}".format(
                serializers.serialize('json', [userdata, ])
            ))
            return redirect('home')
        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
            return render(request, 'verify_phone.html', locals())

    # user_form = UserCreationForm
    return render(request, 'verify_phone.html', locals())


@login_required
def sendVrfCode(request):
    """
    Lets a user send a verification code to his phone number
    """
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    user = request.user
    if user.is_active and user.phone_status is False:
        um = user_handler.UserManager()
        UserToken.objects.create(user=user)
        ### Update User Events
        eventhandler = user_handler.UserEventManager()
        extrainfo = dict(
            client_public_ip=client_public_ip,
            client_internal_ip=client_internal_ip
        )
        eventhandler.setevent(request.user, 3, extrainfo)
        ### Send user a SMS stating that his phone has been verified
        um.sendVerfTextApp(user.id)
        logger.debug("Verification code sent to the {0}".format(user.phone))
        return redirect('verifyPhone')
    return redirect('home')


@login_required
def home(request):
    """Post login this is returned and displays user's home page"""
    user = request.user
    ##Acquire all the current open jobs related to the user
    from jobs.handler import JobManager
    jb = JobManager()
    jobs = jb.getAllJobs(user)
    if user.is_staff or user.is_superuser:
        return render(request, 'admin/joblist.html', locals())

    return render(request, 'admin/joblist.html', locals())


@login_required
@is_superuser
def createhandymen(request):
    """
    Allows the staff create a handymen
    """
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        user = request.user

    if request.method == "GET":
        if 'ebuser' in request.GET:
            ebuser = request.GET['ebuser']
            try:
                EarlyBirdUser.objects.get(confirmed=False, phone=ebuser)
            except Exception, e:
                return redirect('home')
            user_form = UserCreationForm(ebuser=ebuser)
            pagetitle = "Create a Handymen"
            return render(request, 'admin/createuser.html', locals())

    if request.method == "POST":
        user_form = UserCreationForm(request.POST, ebuser=None)
        if user_form.is_valid():
            useraddress = dict(
                city=user_form.cleaned_data['city'],
                streetaddress=user_form.cleaned_data['streetaddress']
            )
            userdata = user_form.save(commit=False)
            userdata.address = json.dumps(useraddress)
            userdata.phone_status = True
            userdata.user_type = 1
            userdata.phone = user_form.cleaned_data['phone']
            import hashlib
            import uuid
            hashstring = hashlib.sha256(
                str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())
            ).hexdigest()
            password = hashstring[:4]+hashstring[-2:]
            # password = user_form.cleaned_data['password1']
            userdata.set_password(password)
            userdata.save()
            logger.warn("New handyman {0} has been created.".format(
                userdata.phone.as_international)
            )
            try:
                ebuser = EarlyBirdUser.objects.get(phone=userdata.phone)
                ebuser.confirmed = True
                ebuser.save()
            except Exception as e:
                pass
            return redirect('home')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        pagetitle = "Create a Handyman"
        return render(request, 'admin/createhm.html', locals())
    else:
        user_form = UserCreationForm(ebuser=None)
        pagetitle = "Create a Handymen"
        return render(request, 'admin/createhm.html', locals())


@login_required
@is_superuser
def createUser(request):
    """
    Allows the staffs create a user
    """
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        user = request.user

    if request.method == "GET":
        if 'ebuser' in request.GET:
            ebuser = request.GET['ebuser']
            try:
                EarlyBirdUser.objects.get(confirmed=False, phone=ebuser)
            except Exception, e:
                return redirect('home')
            user_form = UserCreationForm(ebuser=ebuser)
            pagetitle = "Create a User"
            return render(request, 'admin/createuser.html', locals())

    if request.method == "POST":
        user_form = UserCreationForm(request.POST, ebuser=None)
        if user_form.is_valid():
            useraddress = dict(
                city=user_form.cleaned_data['city'],
                streetaddress=user_form.cleaned_data['streetaddress']
            )
            userdata = user_form.save(commit=False)
            userdata.address = json.dumps(useraddress)
            userdata.phone_status = True
            userdata.user_type = 2
            userdata.phone = user_form.cleaned_data['phone']
            import hashlib
            import uuid
            hashstring = hashlib.sha256(
                str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())
            ).hexdigest()
            password = hashstring[:4]+hashstring[-2:]
            # password = user_form.cleaned_data['password1']
            userdata.set_password(password)
            try:
                ebuser = EarlyBirdUser.objects.get(phone=userdata.phone)
                ebuser.confirmed = True
                ebuser.save()
            except Exception as e:
                logger.warn("EB user {0} not found".format(userdata.phone))
                return redirect('index')
            userdata.save()
            um = user_handler.UserManager()
            # Commenting the below for now, user would be notified of
            # their password only after our internal portal is ready
            # um.sendPasswordText(userdata.id, password)
            msg = messages.USER_WELCOME_MSG
            vas = Sparrow()
            status = vas.sendMessage(msg, userdata)
            logger.warn("Message status \n {0}".format(status))
            logger.warn("New user {0} has been created.".format(
                userdata.phone.as_international)
            )
            return redirect('home')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        pagetitle = "Create a Handymen"
        return render(request, 'admin/createuser.html', locals())
    else:
        user_form = UserCreationForm(ebuser=None)
        pagetitle = "Create a Handymen"
        return render(request, 'admin/createuser.html', locals())


@csrf_exempt
def joinasuser(request):
    """
    Early bird Register as a user
    """
    # If a user joins from the web
    if request.method == "POST":
        request_dict = request.POST.copy()
        phone = request_dict.get('phone')
        if phone == '':
            return redirect('index')
        try:
            phone = intlphone.from_string(
                request_dict.get('phone'),
                region='NP')
        except Exception as e:
            return redirect('index')

        request_dict['phone'] = phone
        logging.warn(request_dict)
        user_form = EBUserPhoneNumberForm(request_dict)
        if user_form.is_valid():
            phone = user_form.cleaned_data['phone']
            userdata = user_form.save(commit=False)
            userdata.save()
            logger.warn("{0} registered their number as a user".format(phone))
            vas = Sparrow()
            msg = messages.NEW_USER_REG_MSG
            status = vas.sendDirectMessage(msg, phone)
            logger.warn(status)
            email_handler.send_newregistration_notif(phone.as_international)
            # requests.get(
            #     request.build_absolute_uri(reverse('gaTracker'))
            # )
            return redirect('index')
        if user_form.errors:
            # requests.get(
            #     request.build_absolute_uri(reverse('gaTracker'))
            # )
            logger.debug("Login Form has errors, %s ", user_form.errors)
            return render(request, 'index.html', locals())
        return redirect('index')

    # disbale GET
    return redirect('index')


@csrf_exempt
def smsEndpoint(request):
        # If it's from Sparrow's System or regular GET request
        if 'from' in request.GET:
            phone = urllib.unquote(request.GET['from'])
            userphone = dict(phone=phone)
            text = urllib.unquote(request.GET['text'])
            user_form = EBUserPhoneNumberForm(userphone)
            # If no keyword on the message
            if len(text.lower().split()) == 1 and text.lower().split()[0] in os.environ['SMS_KEYWORD'].split(','):
                if user_form.is_valid():
                    phone = user_form.cleaned_data['phone']
                    userdata = user_form.save(commit=False)
                    userdata.save()
                    logger.warn("{0} just registered their number as a user. \
                        [valid entry]".format(phone))
                    msg = messages.NEW_USER_REG_MSG
                    # send email to admin
                    email_handler.send_newregistration_notif(
                        phone.as_international
                    )
                    requests.get(
                        request.build_absolute_uri(reverse('gaTracker'))
                    )
                    return HttpResponse(msg, content_type="text/html")
                # As of now, error only seems to be in duplicate or wrong phone
                elif user_form.errors:
                    # Check if the account is created for this user
                    try:
                        userdetails = UserProfile.objects.get(phone=phone)
                    except UserProfile.DoesNotExist:
                        try:
                            EarlyBirdUser.objects.get(
                                phone=phone
                            )
                            msg = messages.DUP_USER_REG_MSG
                            logger.warn("{0} duplicate user creation request. \
                            [account being processed]".format(phone))
                            requests.get(
                                request.build_absolute_uri(reverse('gaTracker'))
                            )
                            return HttpResponse(msg, content_type="text/html")
                        except EarlyBirdUser.DoesNotExist:
                            msg = "Invalid Input!"
                            logger.warn("{0} sent an invalid request, [Invalid Input]".format(request.META['REMOTE_ADDR']))
                            requests.get(
                                request.build_absolute_uri(reverse('gaTracker'))
                            )
                            return HttpResponse(msg, content_type="text/html")

                    # if account exists consider this as a new job request, the
                    # the call center calls
                    jm = jobs_handler.JobManager()
                    jm.createJob(userdetails)
                    msg = messages.JOB_REQ_MSG
                    logger.warn("{0} just requested for a service. \
                    [valid user]".format(phone))
                    # send email and SMS to admin
                    vas = Sparrow()
                    adminmsg = "Request for service received from {0}".format(
                        userdetails.phone.as_national
                    )
                    vas.sendDirectMessage(
                        adminmsg, intlphone.from_string('+9779802036633')
                    )
                    email_details = email_handler.prepNewJobRegistrationNotification(
                        userdetails.phone.as_international, userdetails.name
                    )
                    email_handler.send_email_admin(email_details)
                    requests.get(
                        request.build_absolute_uri(reverse('gaTracker'))
                    )
                    return HttpResponse(msg, content_type="text/html")
            elif len(text.lower().split()) > 1:
                if user_form.is_valid():
                    phone = user_form.cleaned_data['phone']
                    userdata = user_form.save(commit=False)
                    userdata.save()
                    logger.warn("{0} just registered their number as a user. \
                        [valid entry]".format(phone))
                    msg = messages.NEW_USER_REG_MSG
                    # send email to admin
                    email_handler.send_newregistration_notif(
                        phone.as_international
                    )
                    requests.get(
                        request.build_absolute_uri(reverse('gaTracker'))
                    )
                    return HttpResponse(msg, content_type="text/html")
                # As of now, error only seem to be in duplicate phone number
                elif user_form.errors:
                    # Check if the account is created for this user
                    try:
                        userdetails = UserProfile.objects.get(phone=phone)
                    except UserProfile.DoesNotExist:
                        try:
                            EarlyBirdUser.objects.get(
                                phone=phone
                            )
                            msg = messages.DUP_USER_REG_MSG
                            logger.warn("{0} duplicate user creation request. \
                            [account being processed]".format(phone))
                            requests.get(
                                request.build_absolute_uri(reverse('gaTracker'))
                            )
                            return HttpResponse(msg, content_type="text/html")
                        except EarlyBirdUser.DoesNotExist:
                            msg = "Invalid Input!"
                            logger.warn("{0} sent an invalid request, [Invalid Input]".format(request.META['REMOTE_ADDR']))
                            requests.get(
                                request.build_absolute_uri(reverse('gaTracker'))
                            )
                            return HttpResponse(msg, content_type="text/html")
                    # if account exists consider this as a new job request, the
                    # the call center calls
                    jm = jobs_handler.JobManager()
                    jm.createJob(userdetails)
                    msg = messages.JOB_REQ_MSG
                    logger.warn("{0} just requested for a service. \
                    [valid user]".format(phone))
                    # send email and SMS to admin
                    vas = Sparrow()
                    adminmsg = "Request for service received from {0}".format(
                        userdetails.phone.as_national
                    )
                    vas.sendDirectMessage(
                        adminmsg,
                        intlphone.from_string('+9779802036633')
                    )
                    email_details = email_handler.prepNewJobRegistrationNotification(
                        userdetails.phone.as_international,
                        userdetails.name
                    )
                    email_handler.send_email_admin(email_details)
                    requests.get(
                        request.build_absolute_uri(reverse('gaTracker'))
                    )
                    return HttpResponse(msg, content_type="text/html")
            else:
                msg = "Invalid Input!"
                logger.warn("{0} sent a invalid request, [Invalid Input]".format(phone))
                requests.get(
                    request.build_absolute_uri(reverse('gaTracker'))
                )
                return HttpResponse(msg, content_type="text/html")

        msg = "Invalid Input!"
        logger.warn("{0} sent an invalid request, [Invalid Input]".format(request.META['REMOTE_ADDR']))
        requests.get(
            request.build_absolute_uri(reverse('gaTracker'))
        )
        return HttpResponse(msg, content_type="text/html")

# @csrf_exempt
# def joinashandymen(request):
#     """
#     Early bird Register as a handymen
#     """
#     if request.method == "POST":
#         user_form = HMUserPhoneNumberForm(request.POST)
#         if user_form.is_valid():
#             phone = user_form.cleaned_data['phone']
#             userdata = user_form.save(commit=False)
#             userdata.save()
#             logger.warn("{0} just registered their number as a handymen".format(phone))
#             vas = Sparrow()
#             msg = "Thankyou for registering with The Right Handyman! Please expect a call soon for further processing!"
#             status = vas.sendDirectMessage(msg, phone)
#             logger.warn(status)
#             email_handler.send_newregistration_notif(phone.as_international)
#             return redirect('index')
#
#         if user_form.errors:
#             logger.debug("Login Form has errors, %s ", user_form.errors)
#         return redirect('index')
#     return redirect('index')


@login_required
def myProfile(request):
    """
    Displays profile of the logged in user
    """
    user = request.user
    um = user_handler.UserManager()
    userdetails = um.getUserDetails(user.id)
    return render(request, 'profilepage.html', locals())


def gaTracker(request):
    """
    Returns the page with GA javascript, helps track conversion
    """
    return render(request, "registerresponse.html", locals())


@login_required
@is_superuser
def viewEBUser(request):
    """
    Returns a list of Early Bird Users
    """
    user = request.user
    um = user_handler.UserManager()
    ebusers = um.getEBUserList()
    return render(request, "admin/betauserlist.html", locals())


@login_required
def userSettings(request):
    """
    Change user profile settings
    """
    user = request.user
    userdata = dict(
        name=user.name,
        phone=user.phone,
        city=user.address['city'],
        streetaddress=user.address['streetaddress']
    )

    if request.method == "POST":
        user = request.user
        um = user_handler.UserManager()
        userdetails = um.getUserDetails(user.id)
        user_form = HMUserChangeForm(request.POST, instance=userdetails)
        oldaddress = userdetails.address
        if user_form.is_valid():
            userdata = user_form.save(commit=False)
            address = {}
            address['city'] = user_form.cleaned_data['city']
            address['streetaddress'] = user_form.cleaned_data['streetaddress']
            userdata.address = address
            userdata.save()
            userdetails = um.getUserDetails(user.id)
            newaddress = userdetails.address
            if newaddress != oldaddress:
                userdetails.address_coordinates = userdetails.get_lat_long(address)
                userdetails.save()
            logger.warn(userdetails.address_coordinates)
            return redirect('userSettings')

        if user_form.errors:
            logger.debug("UserSettings form has erorrs %s", user_form.errors)
            return render(request, "usersettings.html", locals())

    user_form = HMUserChangeForm(initial=userdata)
    return render(request, "usersettings.html", locals())
