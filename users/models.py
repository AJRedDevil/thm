

#All Django Imports
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.gis.db import models
from django.core.files import File
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils import six


#All external imports (libs, packages)
import hashlib
import os
import uuid
import simplejson as json
import time
import jsonfield
import logging
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

# Init Logger
logger = logging.getLogger(__name__)

CITY_SELECTION = (
    ('Kathmandu', 'Kathmandu'),
    ('Lalitpur', 'Lalitpur'),
    ('Bhaktapur', 'Bhaktapur'),
)

# Create your models here.


class UserManager(BaseUserManager, models.GeoManager):

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password,
        user verifies the phone with a authcode.
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
        address = dict(
            streetaddress='Thirbum Marg - 4, Baluwatar',
            city='Kathmandu'
        )
        u = self._create_user(phone, password, address=address, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.phone_status = True
        u.user_type = 0
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


def getUniqueUUID():
    uniqueID = ''.join(str(uuid.uuid4()).split('-'))
    return uniqueID


class UserProfile(AbstractBaseUser):
    """
    User Profile
    """

    def __get_pp_path(self, profile_image):
        return 'avatars/'+str(self.userref[8:24])+'/'+str(self.__generate_hash()[:8]+'.jpg')

    id = models.AutoField(_('id'), primary_key=True)
    userref = models.CharField(
        _('userref'),
        max_length=100,
        unique=True,
        default=getUniqueUUID
    )
    name = models.CharField(_('name'), max_length=30)
    phone_status = models.BooleanField(_('phone_status'), default=False)
    phone = PhoneNumberField(_('phone'), max_length=16, unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    profile_image = models.ImageField(
        max_length=1024,
        upload_to=__get_pp_path,
        blank=True,
        default=''
    )
    """Account Status"""
    # 1 = Active
    # 0 = Suspended
    account_status = models.IntegerField(
        _('account_status'),
        max_length=1,
        default=1
    )
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
    address_coordinates = models.PointField(
        _('address_coordinates'),
        srid=4326,
        default='',
        blank=True,
        null=True
    )
    current_address = models.PointField(
        _('current_address'),
        srid=4326,
        default='',
        blank=True,
        null=True
    )
    extrainfo = jsonfield.JSONField(
        _('extrainfo'),
        default='{}',
        max_length=9999
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __unicode__(self):
        return str(self.name+' ('+str(self.phone)+')')

    def get_name(self):
        return self.name

    def thumbnail_exists(self):
        from django.core.files.storage import default_storage as storage
        return storage.exists(
            os.path.join(
                settings.MEDIA_ROOT,
                os.path.splitext(
                    self.profile_image.name.lower())[0]+'_normal.jpeg'))

    def __generate_hash(self):
        return hashlib.sha256(
            str(self.date_joined) + str(time.time())).hexdigest()

    def get_lat_long(self, address):
        from libs.googleapi_handler import GeoCoding
        gc = GeoCoding()
        return gc.get_lat_long(address)

    def get_profile_pic(self):
        if storage.exists(os.path.join(
                settings.MEDIA_ROOT,
                os.path.splitext(
                            self.profile_image.name.lower())[0]+'_normal.jpeg')):
            return storage.url(self.profile_image.name.split('.')[0])+'_normal.jpeg'
        return "/static/img/logo.png"

    def create_thumbnail(self, size=400, quality=None):
        if self.profile_image != '':
            try:
                from PIL import Image
                from cStringIO import StringIO
                self.profile_image.seek(0)
                orig = self.profile_image.read()
                image = Image.open(StringIO(orig))
                quality = 85
                w, h = image.size
                if w != size or h != size:
                    if w > h:
                        diff = int((w - h) / 2)
                        image = image.crop((diff, 0, w - diff, h))
                    else:
                        diff = int((h - w) / 2)
                        image = image.crop((0, diff, w, h - diff))
                    if image.mode != "RGB":
                        image = image.convert("RGB")
                    image = image.resize((size, size), Image.ANTIALIAS)
                    # thumb = six.BytesIO()
                    file_path = os.path.join(
                        settings.MEDIA_ROOT,
                        os.path.splitext(self.profile_image.name.lower())[0]+'_normal.jpeg'
                        )
                    image.save(file_path, 'JPEG', quality=quality)
                    # thumb_file = ContentFile(thumb.getvalue())
                # else:
                    # thumb_file = File(orig)
                file_path = os.path.join(
                    settings.MEDIA_ROOT,
                    os.path.splitext(self.profile_image.name.lower())[0]+'_normal.jpeg'
                    )
                image.save(file_path, 'JPEG', quality=quality)
            except Exception, e:
                # logger.warn('file not found')
                logger.warn(e)
                return  # What should we do here?  Render a "sorry, didn't work" img?

    def save(self, *args, **kwargs):
        if type(self.address) != dict:
            self.address = json.loads(self.address)
        if self.address_coordinates == '' or self.address_coordinates is None:
            myLatLng = self.get_lat_long(self.address)
            self.address_coordinates = "POINT("+str(myLatLng['lng'])+" \
                "+str(myLatLng['lat'])+")"
        # self.create_thumbnail()
        super(UserProfile, self).save(*args, **kwargs)

# Create Token for users when a user is created
@receiver(post_save, sender=UserProfile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserEvents(models.Model):
    """Models for Users UserEvents"""

    user = models.ForeignKey(UserProfile)
    event = models.IntegerField(_('event'), max_length=2, default=1)
    updated_on = models.DateTimeField(
        _('updated_on'),
        default=timezone.now
    )
    extrainfo = jsonfield.JSONField(
        _('extrainfo'),
        default='{}',
        max_length=9999
    )

    def save(self, *args, **kwargs):
        super(UserEvents, self).save(*args, **kwargs)


class EarlyBirdUser(models.Model):
    """
    List of customers who registered in the early phase
    """

    phone = PhoneNumberField(_('phone'), max_length=16, unique=True)
    registered_on = models.DateTimeField(
        _('updated_on'),
        default=timezone.now
    )
    confirmed = models.BooleanField(_('confirmed'), default=False)

    def __unicode__(self):
        return self.phone

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
    Token Model Class for user's verification,
    password reset and other such services
    """
    user = models.ForeignKey(UserProfile)
    token = models.CharField(_('id'), max_length=20, primary_key=True)
    timeframe = models.DateTimeField(_('timeframe'), default=timezone.now)
    status = models.BooleanField(_('status'), default=False)
    tokentype = models.IntegerField(_('0'), default=0)

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
        strhash = hashlib.sha256(
            str(timezone.now()) + str(uuid.uuid4())).hexdigest()[:14]
        randnum = str(randint(123456, 999889))
        return strhash+randnum

    def __unicode__(self):
        return self.token

    # Overriding
    def save(self, *args, **kwargs):
        # Tag all existing tokens from this user as used before creating new
        UserToken.objects.filter(user_id=self.user).update(status=True)
        self.token = self.generate_token()
        super(UserToken, self).save(*args, **kwargs)
