from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from accounts.forms import MySignupForm
from django.contrib.sites.shortcuts import get_current_site
from profile_app.models import Profile
from django.core.exceptions import FieldDoesNotExist, ValidationError



import logging
logger = logging.getLogger(__name__)


class MyAccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(
            request,
            emailconfirmation)
        try:
            logger.info("パスワードを表示する：{}".format(request.password))        
            ctx = {
               "user": emailconfirmation.email_address.user,
               "activate_url": activate_url,
              "current_site": current_site,
              "key": emailconfirmation.key,
              "last_name": request.last_name,
             "password": request.password,
            }
        except AttributeError:
            ctx = {
                "user": emailconfirmation.email_address.user,
                "activate_url": activate_url,
                "current_site": current_site,
                "key": emailconfirmation.key,
            }

        if signup:
            email_template = 'account/email/email_confirmation_signup'
        else:
            email_template = 'account/email/email_confirmation'
        self.send_mail(email_template,
                       emailconfirmation.email_address.email,
                       ctx)
    
    def save_profile(self, request, user, form, commit=True):
        """プロフィールレコードをCreatする"""
        #profile_last_name, profile_first_name#, profile_department
        #pass

        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        #profile_first_name(user, first_name)
        #profile_last_name(user, last_name)
        #profile_department(user, email)
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user

#def profile_first_name(user, *args):
#    return MySetter(user, app_settings.USER_MODEL_EMAIL_FIELD, *args)

"""
def MySetter(user, field, *args):
    try:
        field_meta = Profile._meta.get_field(field)
        max_length = field_meta.max_length
    except FieldDoesNotExist:
        if not hasattr(user, field):
            return
        max_length = None
    v = args[0]
    if v:
        v = v[0:max_length]
        setattr(user, field, v)

#####
    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings,
                         'ALLAUTH_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, dflt))
        return getter(self.prefix + name, dflt)

    @property
    def USER_MODEL_EMAIL_FIELD(self):
        return self._setting('USER_MODEL_EMAIL_FIELD', 'email')
"""
