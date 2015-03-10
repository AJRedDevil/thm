from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import default_storage as storage
from django.conf import settings
from jobs.models import Jobs
import os
import time
import hashlib


class JobGalleryImages(models.Model):
    """
    Gallery Images model
    """
    def __get_path(self, image):
        return 'job_assets/'+str(self.__generate_hash()[:8]+'.jpg')

    def __generate_hash(self):
        return hashlib.sha256(str(time.time())).hexdigest()

    job = models.ForeignKey(Jobs, related_name="gallery")

    image = models.ImageField(
        max_length=1024,
        upload_to=__get_path,
        blank=True,
        default=''
    )
    img_type = models.IntegerField(_('Image Type'), max_length=2, default=1)

    def get_img_url(self):
        if storage.exists(os.path.join(
                settings.MEDIA_ROOT, self.image.name)):
            return storage.url(self.image.name)


#     """
#     Model for Job Gallery
#     """
#     job = models.ForeignKey(Jobs, related_name="gallery")
#     before = models.ForeignKey(JobGalleryImages, related_name='before')
#     after = models.ForeignKey(JobGalleryImages, related_name='after')
