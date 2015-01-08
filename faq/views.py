from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from thm.decorators import is_superuser

from .models import FAQManager
from .forms import FAQCreationForm
import logging
# Init Logger
logger = logging.getLogger(__name__)

# Create your views here.

def faq(request):
    """
    Returns Public FAQ Page
    """
    fm = FAQManager()
    faqs = fm.all()
    return render(request, 'faq.html', locals())

@login_required
@is_superuser
def viewAllFaq(request):
    user = request.user
    fm = FAQManager()
    allfaq = fm.all()
    logger.warn(allfaq)
    return render(request, 'allfaq.html', locals())

@login_required
@is_superuser
def createFaq(request):
    user = request.user
    if request.method == "POST":
        faq_form = FAQCreationForm(request.POST)
        if faq_form.is_valid():
            faq_form.save()

        if faq_form.errors:
            logger.debug("Form has errors, %s ", faq_form.errors)

    faq_form = FAQCreationForm()
    return render(request, 'createfaq.html', locals())

@login_required
@is_superuser
def viewFaq(request, faq_id):
    user = request.user
    faq = FAQ.objects.get(faqref=faq_id)
    if request.method=="POST":
        faq_form = FAQCreationForm(request.POST)
        if faq_form.is_valid():
            faq = FAQ.objects.get(faqref=faq_id)
            faq_form = FAQCreationForm(request.POST, instance=faq)
            logger.debug(faq_form.errors)
            faq_form.save()

        if faq_form.errors:
            logger.debug("Form has errors, %s ", faq_form.errors)

    faq_form = FAQCreationForm(instance=faq)
    return render(request, 'viewfaq.html', locals())
