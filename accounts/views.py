from allauth.account.views import ConfirmEmailView, SignupView
from allauth.account import app_settings
from django.shortcuts import redirect
from django.contrib import messages

# MySignupView用：
# from allauth.account.adapter import get_adapter
from accounts.forms import MySignupForm
from profile_app.models import Profile
from profile_app.forms import ProfileCreateForm

from django.views.generic.edit import FormView
from allauth.account.views import AjaxCapableProcessFormViewMixin



import logging
logger = logging.getLogger(__name__)


class MyConfirmEmailView(ConfirmEmailView):
    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # 「ww14@ww.com は確認されました。」メッセージを消す
        # get_adapter(self.request).add_message(self.request, messages.SUCCESS,
        # 'account/messages/email_confirmed.txt', {'email': confirmation.email_address.email})
        if app_settings.LOGIN_ON_EMAIL_CONFIRMATION:
            resp = self.login_on_confirm(confirmation)
            if resp is not None:
                return resp
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)


class MySignupView(SignupView):
#class MySignupView(generic.ListView, generic.edit.ModelFormMixin):
    form_class =MySignupForm
    #form_class2 =ProfileEditForm

    def get_context_data(self, **kwargs):
       context= SignupView.get_context_data(self, **kwargs)
       #form2 = self.form_class2(self.request.POST or None)
       #context.update({'form2':form2})
       return context

"""
class ProfileformView(AjaxCapableProcessFormViewMixin, FormView):
    def get_ajax_data(self):
        data = []
        for emailaddress in self.request.user.emailaddress_set.all():
            data.append({
                'id': emailaddress.pk,
                'email': emailaddress.email,
                'verified': emailaddress.verified,
                'primary': emailaddress.primary,
            })
        return data
"""
