from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

def getUniqueUUID():
    uniqueID = ''.join(str(uuid.uuid4()).split('-'))
    return uniqueID

class FAQ(models.Model):
    """docstring for FAQ"""
    faqref = models.CharField(_('faqref'), max_length=100, unique=True,
        default=getUniqueUUID)
    question = models.TextField(_('question'))
    answer = models.TextField(_('answer'))

    def __unicode__(self):
        return self.id


class FAQManager(object):
    """
    Manager for FAQ
    """
    def all(self):
        return FAQ.objects.filter().order_by('id')
