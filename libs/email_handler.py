import logging
# logging.basicConfig()
logger = logging.getLogger(__name__)

from django.core.mail import EmailMessage
from django.conf import settings

def _prepNewUserRegistrationNotification(phone):
    """Prepare the details for notification emails after new user registers"""
    template_name="New_User_Registration"
    subject="THM - New User Registered !"
    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'phone_number'   : phone,
                                                },
                    }

    return email_details

def prepNewJobRegistrationNotification(phone, name=None):
    """Prepare the details for notification emails after new job requests are put via SMS or App"""
    template_name="New_Job_Registration"
    subject="THM - New Job Registered !"
    email_details = {
                        'subject' : subject,
                        'template_name' : template_name,
                        'global_merge_vars': {
                                                'phone_number'   : phone,
                                                'name'  : name
                                                },
                    }

    return email_details

def _load_template(user, email_details):
    """
    Loads the email contents and returns the template for email
    """
    ##Email Template Init###
    email_template = EmailMessage(
        subject=email_details['subject'],
        from_email="The Homerepair App <do-not-reply@thehomerepairapp.com>",
        to=[user,]
        )

    ###List Email Template###
    email_template.template_name = email_details['template_name']

    ###List Email Tags to be used###
    email_template.global_merge_vars = email_details['global_merge_vars']

    return email_template

def send_newregistration_notif(phone):
    """
    Send a notification email to the user.
    """
    user = settings.ADMIN_EMAIL
    try:
        email_details = _prepNewUserRegistrationNotification(phone)
        msg = _load_template(user, email_details)
        msg.send()
        logger.warn("Notification sent to - %s for %s", user, email_details['template_name'])
        return "success"
    except Exception, e:
        logger.warn("Error during sending of Email to - %s for %s", user, email_details['template_name'])
        logger.warn("Error message is %s", str(e))
        return "fail"

def send_email_admin(email_details):
    """
    Sends an email to admin 
    """
    user = settings.ADMIN_EMAIL
    try:
        msg = _load_template(user, email_details)
        msg.send()
        logger.debug("Notification sent to - %s for %s", user, email_details['template_name'])
    except Exception, e:
        logger.warn("Error during sending of Email to - %s for %s", user, email_details['template_name'])
        logger.warn("Error message is %s", str(e))
        return "fail"
