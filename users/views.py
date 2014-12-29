

#All Djang Imports
# from django.conf import settings
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
# from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

#All local imports (libs, contribs, models)
import handler as user_handler
from thm.decorators import is_superuser
from .models import UserProfile, EarlyBirdUser, UserToken
from .forms import UserCreationForm, LocalAuthenticationForm, EBUserPhoneNumberForm, HMUserPhoneNumberForm, VerifyPhoneForm

#All external imports (libs, packages)
from libs.sparrow_handler import Sparrow
from libs import email_handler
from ipware.ip import get_real_ip, get_ip
import simplejson as json
import logging
import urllib


# Init Logger
logger = logging.getLogger(__name__)


# Create your views here.
def logout(request):
    """Logs out the user"""
    user = request.user
    if user.is_authenticated:
        eventhandler = user_handler.UserEventManager()
        extrainfo = dict()
        eventhandler.setevent(user, 0, extrainfo)
        auth_logout(request)
    return redirect('index')
    
def signin(request):
    """
    View to login to the portal
    """
    ## if authenticated redirect to user's homepage directly ##
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    if request.GET:  
        next = request.GET['next']

    if request.user.is_authenticated():
        return redirect('home')

    if request.method == "POST":   
        auth_form = LocalAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            auth_login(request, auth_form.get_user())
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(client_public_ip=client_public_ip, client_internal_ip=client_internal_ip)
            eventhandler.setevent(request.user, 1, extrainfo)
            #Notify the user of his status if he's unavailable
            if request.user.is_authenticated():
                    if request.POST.get('next'):
                        return HttpResponseRedirect(request.POST.get('next'))
                    return redirect('home')
            return redirect('home')

        if auth_form.errors:
            logger.debug("Login Form has errors, %s ", auth_form.errors)
    return render(request, 'signin.html', locals())


def signup(request):
    """
    Lets a user signup 
    """
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            userdata = user_form.save(commit=False)
            userdata.address = dict(city=user_form.cleaned_data['city'], streetaddress=\
                user_form.cleaned_data['streetaddress'])
            userdata.save()
            authenticate(username=userdata.phone, password=userdata.password)
            userdata.backend='django.contrib.auth.backends.ModelBackend'
            auth_login(request, userdata)
            UserToken.objects.create(user=userdata)
            eventhandler = user_handler.UserEventManager()
            extrainfo = dict(client_public_ip=client_public_ip, client_internal_ip=client_internal_ip)
            eventhandler.setevent(request.user, 1, extrainfo)
            um = user_handler.UserManager()
            um.sendVerfText(userdata.id)
            logger.debug("user created")
            logger.debug("User Details : \n {0}".format(serializers.serialize('json',[userdata, ])))
            return redirect('home')
        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
            return render(request, 'signup.html', locals())

    user_form = UserCreationForm
    return render(request, 'signup.html', locals())

@login_required
def verifyPhone(request):
    """
    Lets a user verify his phone number 
    """
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    user = request.user
    if user.phone_status == True:
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
            extrainfo = dict(client_public_ip=client_public_ip, client_internal_ip=client_internal_ip)
            eventhandler.setevent(request.user, 2, extrainfo)                
            ### Send user a SMS stating that his phone has been verified
            um.sendPhoneVerfText(user.id)
            logger.debug("User's phone verified")
            logger.debug("User Details : \n {0}".format(serializers.serialize('json',[userdata, ])))
            return redirect('home')
        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
            return render(request, 'verify_phone.html', locals())

    user_form = UserCreationForm
    return render(request, 'verify_phone.html', locals())

@login_required
def sendVrfCode(request):
    """
    Lets a user send a verification code to his phone number 
    """
    client_internal_ip = get_real_ip(request)
    client_public_ip = get_ip(request)
    user = request.user
    if user.is_active and user.phone_status == False:
        um = user_handler.UserManager()
        UserToken.objects.create(user=user)
        ### Update User Events
        eventhandler = user_handler.UserEventManager()
        extrainfo = dict(client_public_ip=client_public_ip, client_internal_ip=client_internal_ip)
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
    return render(request,'homepage.html', locals())

@login_required
@is_superuser
def createhandymen(request):
    """Signup, if request == POST, creates the user"""
    ## if authenticated redirect to user's homepage directly ##
    if request.user.is_authenticated():
        user = request.user

    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            useraddress = dict(city=user_form.cleaned_data['city'], streetaddress=user_form.cleaned_data['streetaddress'])
            userdata = user_form.save(commit=False)
            userdata.address = json.dumps(useraddress)
            userdata.phone_status = True
            userdata.user_type = 1
            userdata.phone = user_form.cleaned_data['phone']
            # import hashlib
            # import uuid
            # hashstring = hashlib.sha256(str(timezone.now()) + str(timezone.now()) + str(uuid.uuid4())).hexdigest()
            # password = hashstring[:4]+hashstring[-2:]
            password = user_form.cleaned_data['password1']
            userdata.set_password(password)
            userdata.save()
            vas = Sparrow()
            msg = "Thankyou {0} for registering with The Right Handyman! Your account is being processed!".format(userdata.first_name)
            status = vas.sendMessage(msg, UserProfile.objects.get(phone=userdata.phone))
            logger.warn(status)
            return redirect('home')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        pagetitle = "Create a Handymen"
        return render(request, 'createhandymen.html', locals())
    else:
        user_form = UserCreationForm()
        pagetitle = "Create a Handymen"
        return render(request, 'createhandymen.html', locals())

@csrf_exempt
def joinasuser(request):
    """
    Early bird Register as a user 
    """
    # If a user joins from the web
    if request.method == "POST":
        user_form = EBUserPhoneNumberForm(request.POST)
        if user_form.is_valid():
            phone = user_form.cleaned_data['phone']
            userdata = user_form.save(commit=False)
            userdata.save()
            logger.warn("{0} just registered their number as a user".format(phone))
            vas = Sparrow()
            msg = "Thankyou for registering with The Right Handyman! We shall inform you once we are operational!"
            status = vas.sendDirectMessage(msg, phone)
            logger.warn(status)
            email_handler.send_newregistration_notif(phone.as_international)
            return redirect('index')
        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        return redirect('index')

    # If it's from Sparrow's System or regular GET request
    if request.GET.has_key('from'):
        phone = urllib.unquote(request.GET['from'])
        userphone = dict(phone=phone)
        text = urllib.unquote(request.GET['text'])
        user_form = EBUserPhoneNumberForm(userphone)
        # If no keyword on the message
        if len(text.lower().split()) == 1 and text.lower().split()[0]=='handyman':
            if user_form.is_valid():
                phone = user_form.cleaned_data['phone']
                userdata = user_form.save(commit=False)
                userdata.save()
                logger.warn("{0} just registered their number as a user".format(phone))
                msg = "Thankyou for registering with The Right Handyman! We shall inform you once we are operational!"
                # logger.warn(phone)
                # send email to admin
                email_handler.send_newregistration_notif(phone.as_international)
                return HttpResponse(msg,content_type="text/html")
            # As of now, error only seem to be in duplicate data
            elif user_form.errors:
                msg = "You seem to have been registered already! We would get back to you soon!"
                logger.debug("Login Form has errors on GET for /register, %s ", user_form.errors)
                return HttpResponse(msg,content_type="text/html")                
        elif len(text.lower().split()) > 1:
            try:
                ebuser = EarlyBirdUser.objects.get(phone=phone)
            except EarlyBirdUser.DoesNotExist:
                user_form = EBUserPhoneNumberForm(userphone)
                if user_form.is_valid():
                    phone = user_form.cleaned_data['phone']
                    userdata = user_form.save(commit=False)
                    userdata.save()
                    logger.warn("{0} just registered their number as a user".format(phone))
                    msg = "Thankyou for registering with The Right Handyman! We shall inform you once we are operational!"
                    logger.warn(phone)
                    # send email to admin
                    email_handler.send_newregistration_notif(phone.as_international)
                    return HttpResponse(msg,content_type="text/html")
            memberlist = EarlyBirdUser.objects.all()
            if ebuser in memberlist:
                if text.lower().split()[1]=='plumber':
                    msg = "Request for a plumber received and is queued for processing, a plumber would be put in touch with you soon!"
                    return HttpResponse(msg,content_type="text/html")
                if text.lower().split()[1]=='electrician':
                    msg = "Request for an electrician received and is queued for processing, an electrician would be put in touch with you soon!"
                    return HttpResponse(msg,content_type="text/html")
                # If there are any added, consider it invalid
                else: 
                    msg = "Invalid Input!"
                    return HttpResponse(msg,content_type="text/html")
            else: 
                msg = "Invalid Input!"
                return HttpResponse(msg,content_type="text/html")

    return redirect('index')

@csrf_exempt
def joinashandymen(request):
    """
    Early bird Register as a handymen 
    """
    if request.method == "POST":
        user_form = HMUserPhoneNumberForm(request.POST)
        if user_form.is_valid():
            phone = user_form.cleaned_data['phone']
            userdata = user_form.save(commit=False)
            userdata.save()
            logger.warn("{0} just registered their number as a handymen".format(phone))
            vas = Sparrow()
            msg = "Thankyou for registering with The Right Handyman! Please expect a call soon for further processing!"
            status = vas.sendDirectMessage(msg, phone)
            logger.warn(status)
            email_handler.send_newregistration_notif(phone.as_international)
            return redirect('index')

        if user_form.errors:
            logger.debug("Login Form has errors, %s ", user_form.errors)
        return redirect('index')
    return redirect('index')
