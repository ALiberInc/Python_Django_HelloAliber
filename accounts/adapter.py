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
            logger.debug("パスワードを表示する：{}".format(request.password))        
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

        data = form.cleaned_data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
        return user

    def get_login_redirect_url(self, request):
        if request.user.is_staff:
           logger.debug("{}は　管理者としてログインした".format(request.user.last_name))
           return '/employee_list'
        else:
            logger.debug("{}は　一般社員としてログインした".format(request.user.last_name))
            try:
                user_id = Profile.objects.get(id_id__exact=request.user.id).user_id
            except:
                user_id = -1
            path = "/employee/{user_id}/"
            return path.format(user_id=user_id)

