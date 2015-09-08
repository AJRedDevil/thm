

import hashlib
import jsonfield
import os
import time


from django.conf import settings
from django.core.files.storage import default_storage as storage
from django.db import models
from djmoney.models.fields import MoneyField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.users.models import UserProfile

# Create your models here.


class Inventory(models.Model):
    """Inventory model for keeping track of items.
    """
    name = models.CharField(
        _('name'),
        max_length=100,
        default="",
        blank=False
        )

    #Image
    def __get_path(self, image):
        return 'inventory_assets/' + str(self.__generate_hash()[:8]+'.jpg')

    def __generate_hash(self):
        return hashlib.sha256(
            str(time.time()) + str(self.image.name)
        ).hexdigest()

    image = models.ImageField(
      max_length = 1024,
      upload_to = __get_path,
      blank = True,
      default = ''
    )

    def get_img_url(self):
        if storage.exists(os.path.join(
                settings.MEDIA_ROOT, self.image.name)):
            return storage.url(self.image.name)

    def __unicode__(self):
        return self.name

class ToolInventory(models.Model):
    """ToolInventory model to keep track of inventory to handyman
    """
    handyman = models.ForeignKey(
                UserProfile,
                related_name='toolHolder'
                )
    tools =  models.ManyToManyField(Inventory, blank=True, null=True, related_name='handset')


    