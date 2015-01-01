

#All Django Imports
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
# from django.utils import six

#All external imports (libs, packages)
import hashlib
import uuid
import simplejson as json
import jsonfield
import logging
import pytz
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

# Init Logger
logger = logging.getLogger(__name__)

CITY_SELECTION = (('Kathmandu','Kathmandu'),)

# Create your models here.
class UserManager(BaseUserManager):

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password, user verifies the phone with a authcode.
        Access to service is limited till the user verifies his phone number
        """
        now = timezone.now()

        if not phone:
            raise ValueError('A valid mobile number must be provided')
            
        user = self.model(phone=phone,
                          is_active=True, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        u = self._create_user(phone, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.phone_status = True
        u.save(using=self._db)
        return u

    def create_staffuser(self, phone, password=None, **extra_fields):
        u = self._create_user(phone, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.phone_status = True
        u.save(using=self._db)
        return u

    def create_user(self, phone, password=None, **extra_fields):
        return self._create_user(phone, password, **extra_fields)



class UserProfile(AbstractBaseUser):

    def upload_pp_path(self, name):
        # name = 'pp'
        folder = self.id
        return str(folder) + '/' + str(name)

    id = models.AutoField(_('id'), primary_key=True)
    userref = models.CharField(_('userref'), max_length=100, unique=True, 
        default=''.join(str(uuid.uuid4()).split('-')))
    # displayname = models.CharField(_('displayname'), max_length=30, unique=True, 
    #     error_messages={'unique' : 'The username provided is already taken !'})
    name = models.CharField(_('first_name'), max_length=30)
    # last_name = models.CharField(_('last_name'), max_length=30)
    # email = models.EmailField(_('email'), max_length=100,
    #     error_messages={'unique' : 'It seems you already have an account registered with that email!'})
    phone_status = models.BooleanField(_('phone_status'), default=False)
    phone = PhoneNumberField(_('phone'), max_length=16, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    profile_image = models.ImageField(max_length=1024, upload_to=upload_pp_path, blank=True, default='')
    """Account Status"""
    # 1 = Active
    # 0 = Suspended
    account_status = models.IntegerField(_('account_status'), max_length=1, default=1)
    """User Types"""
    # 0 = THM Staffs
    # 1 = Handymen
    # 2 = Households/Businesses
    # 3 = Contractors
    user_type = models.IntegerField(_('user_type'), default=2)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)
    is_active = models.BooleanField(default=True)
    address = jsonfield.JSONField(_('address'), default='{}', max_length=9999)
    current_address = jsonfield.JSONField(_('current_address'), default='{}', max_length=9999)
    extrainfo = jsonfield.JSONField(_('extrainfo'), default='{}', max_length=9999)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __unicode__(self):
        return str(self.phone) 

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def thumbnail_exists(self, size):
        from django.core.files.storage import default_storage as storage
        return storage.exists(self.profile_image.name)

    def __generate_hash(self):
        return hashlib.sha256(str(self.date_joined) + str(self.phone)).hexdigest()

    def get_lat_long(self, address):
        from libs.googleapi_handler import GeoCoding
        gc = GeoCoding()
        return gc.get_lat_long(address)

    def create_thumbnail(self, size, quality=None):
        # invalidate the cache of the thumbnail with the given size first        
        import os
        from PIL import Image
        from django.core.files.storage import default_storage as storage
        if not self.profile_image:
            logger.debug("No item image available")
            return
        file_path = self.profile_image.name
        filename_base, filename_ext = os.path.splitext(file_path)
        avatar_file_path = ('%s'+'_'+self.__generate_hash()[:10]+'.jpg') % (filename_base)
        try:
            if not storage.exists(avatar_file_path):
                try:    
                    orig = storage.open(file_path, 'rb')            
                    image = Image.open(orig)
                    quality = quality or settings.AVATAR_THUMB_QUALITY
                    w, h = image.size
                    if w > h:
                        diff = int((w - h) / 2)
                        image = image.crop((diff, 0, w - diff, h))
                    else:
                        diff = int((h - w) / 2)
                        image = image.crop((0, diff, w, h - diff))
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    image = image.resize((size, size), Image.ANTIALIAS)
                    # logger.warn(thumb)
                    avatar_image = storage.open(avatar_file_path, "w")
                    image.save(avatar_image, settings.AVATAR_THUMB_FORMAT, quality=quality)
                    avatar_image.close()
                    return avatar_file_path
                except IOError, e:
                    logger.warn(e)
                    return
        except Exception, e:
            return

    def get_profile_pic(self):
        """Returns the url of the profile image"""
        import os
        from django.core.files.storage import default_storage as storage
        default_file_path = settings.STATIC_URL+"img/default.png"
        if not self.profile_image:
            return default_file_path
        file_path = self.profile_image.name
        logger.warn("file path is %s" % file_path)
        filename_base, filename_ext = os.path.splitext(file_path)
        normal_file_path = ('%s'+'_'+self.__generate_hash()[:10]+'.jpg') % (filename_base)

        ##See if the AWS connection exists or works if doesn't return default file path
        try:
            if storage.exists(normal_file_path):
                # logger.debug(storage.url(normal_file_path))
                return storage.url(normal_file_path)
        except Exception:
            return default_file_path

        return default_file_path

    def save(self, *args, **kwargs):
        if type(self.address) != dict:
            self.address = json.loads(self.address)
        if self.current_address == '{}':
            self.current_address = self.get_lat_long(self.address)
        if type(self.current_address) != dict:
            self.current_address = json.loads(self.current_address)

        super(UserProfile, self).save(*args, **kwargs)

        if self.profile_image:
            self.create_thumbnail(500)


# Create Token for users when a user is created
@receiver(post_save, sender=UserProfile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserEvents(models.Model):
    """Models for Users UserEvents"""
    
    user = models.ForeignKey(UserProfile)
    event = models.IntegerField(_('event'), max_length=2, default=1)
    updated_on = models.DateTimeField(_('updated_on'), 
        default=timezone.now)
    extrainfo = jsonfield.JSONField(_('extrainfo'), default='{}', max_length=9999)

    
    def save(self, *args, **kwargs):
        super(UserEvents, self).save(*args, **kwargs)

class EarlyBirdUser(models.Model):
    """
    List of customers who registered in the early phase
    """

    phone = PhoneNumberField(_('phone'), max_length=16, unique=True)
    registered_on = models.DateTimeField(_('updated_on'), 
        default=timezone.now)
    confirmed = models.BooleanField(_('confirmed'), default=False)

    def __unicode__(self):
        return str(self.phone)

    def save(self, *args, **kwargs):
        if not self.registered_on:
            self.registered_on = timezone.now
        super(EarlyBirdUser, self).save(*args, **kwargs)

# class EarlyBirdHandymen(models.Model):
#     """
#     List of Handymen who registered in the early phase
#     """

#     phone = PhoneNumberField(_('phone'), max_length=16, unique=True)
#     registered_on = models.DateTimeField(_('updated_on'), 
#         default=timezone.now)

#     def save(self, *args, **kwargs):
#         if not self.registered_on:
#             self.registered_on = timezone.now
#         super(EarlyBirdHandymen, self).save(*args, **kwargs)

class UserToken(models.Model):
    """
    Token Model Class for user's verification, password reset and other such services
    """
    user = models.ForeignKey(UserProfile)
    token = models.CharField(_('id'), max_length=20, primary_key=True)
    timeframe = models.DateTimeField(_('timeframe'), default=timezone.now)
    status = models.BooleanField(_('status'), default=False)

    def is_alive(self):
        timedelta = timezone.now() - self.timeframe
        days = getattr(settings, 'USER_TOKEN_EXPIRY', None)
        allowable_time = float(days * 24 * 60 * 60)
        return timedelta.total_seconds() < allowable_time

    def get_hash(self):
        return self.token[:14]

    def get_vrfcode(self):
        return self.token[-6:]

    def generate_token(self):
        """
        Generates a token with first 14 hash and last 6 as verification code
        """
        from random import randint
        strhash = hashlib.sha256(str(timezone.now()) + str(uuid.uuid4())).hexdigest()[:14]
        randnum = str(randint(123456,999889))
        return strhash+randnum

    def __unicode__(self):
        return self.token

    # Overriding
    def save(self, *args, **kwargs):
        # Tag all existing tokens from this user as used before creating new
        UserToken.objects.filter(user_id=self.user).update(status=True)
        self.token = self.generate_token()
        super(UserToken, self).save(*args, **kwargs)
