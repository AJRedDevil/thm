from django.conf.urls import patterns,include,url

import apps.faq.views as faqview

urlpatterns = patterns('',
    url(r'^$', faqview.faq, name='faq'),
    url(r'createfaq/$', faqview.createFaq, name='createFaq'),
    url(r'viewallfaq/$', faqview.viewAllFaq, name='viewAllFaq'),
    url(r'(?P<faq_id>\w+)/$', faqview.viewFaq, name='viewFaq'),
)
