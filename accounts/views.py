from allauth.account.views import ConfirmEmailView, LoginView
from allauth.account import app_settings
from django.shortcuts import redirect
from django.contrib import messages

# MySignupView用：
from accounts.forms import MySignupForm
from accounts.models import CustomUser
from profile_app.models import Profile, Department

from profile_app.forms import ProfileCreateForm

from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from allauth.account.views import CloseableSignupMixin, AjaxCapableProcessFormViewMixin, sensitive_post_parameters_m
from allauth.utils import get_form_class, get_request_param
from allauth.account.utils import (
    complete_signup,
    get_login_redirect_url,
    get_next_redirect_url,
    logout_on_password_change,
    passthrough_next_redirect_url,
    perform_login,
    sync_user_email_addresses,
    url_str_to_user_pk,
)

from allauth.exceptions import ImmediateHttpResponse

from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

class MyLoginView(LoginView):
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            #session処理
            username = form.cleaned_data['login']
            logger.debug("user account={}".format(username))
            user_id = CustomUser.objects.get(email__exact=username).id
            is_staff = CustomUser.objects.get(email__exact=username).is_staff
            data = Profile.objects.get(id_id__exact=user_id)
            self.request.session['data'] = data
            self.request.session['user_id'] = user_id
            self.request.session['is_staff'] = is_staff

            return form.login(self.request, redirect_url=success_url)
        except ImmediateHttpResponse as e:
            return e.response


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

      
class MySignupView(CloseableSignupMixin, AjaxCapableProcessFormViewMixin, FormView):
    # allauth/account/view.SignupView 継承した親クラスを削除するため
    template_name = "account/signup." + app_settings.TEMPLATE_EXTENSION
    form_class = form_class = MySignupForm
    redirect_field_name = "next"
    success_url = None

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(MySignupView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'signup', self.form_class)

    def get_success_url(self):
        # Explicitly passed ?next= URL takes precedence
        ret = (
            get_next_redirect_url(
                self.request,
                self.redirect_field_name) or self.success_url)
        return ret

    def form_valid(self, form):
        self.user = form.save(self.request)
        
        #インスタンスの作成
        blank = ""
        logger.debug("ここの部門：{}".format(form.cleaned_data['department_pro']))
        logger.debug("hello : {}".format(CustomUser.objects.get(email = form.cleaned_data['email'])))
        new_profile = Profile.objects.create(
            id = CustomUser.objects.get(email = form.cleaned_data['email']),
            last_name_k = blank,
            first_name_k = blank,
            last_name = form.cleaned_data['last_name'],
            first_name = form.cleaned_data['first_name'],
            gender = 0,
            nationality = blank,
            phone = blank,
            postal_code = blank,
            address1 = blank,
            address2 = blank,
            residence_card = blank,
            health_insurance = blank,
            department_pro = Department.objects.get(department = form.cleaned_data['department_pro']),# from form
            emergency_contact_1_name = blank,
            emergency_contact_1_relationship = blank,
            emergency_contact_1_phone = blank,
            emergency_contact_2_name = blank,
            emergency_contact_2_relationship = blank,
            emergency_contact_2_phone = blank,
            emergency_contact_3_name = blank,
            emergency_contact_3_relationship = blank,
            emergency_contact_3_phone = blank,
            delete = 0,
            create_date = timezone.now(),
            create_id = self.request.user.id,#ログインしているユーザーID
            update_date = timezone.now(),
            update_id = self.request.user.id,)

        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        try:
            return complete_signup(
                self.request, self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super(MySignupView, self).get_context_data(**kwargs)
        form = ret['form']
        email = self.request.session.get('account_verified_email')
        if email:
            email_keys = ['email']
            if app_settings.SIGNUP_EMAIL_ENTER_TWICE:
                email_keys.append('email2')
            for email_key in email_keys:
                form.fields[email_key].initial = email
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        redirect_field_name = self.redirect_field_name
        redirect_field_value = get_request_param(self.request,
                                                 redirect_field_name)
        ret.update({"login_url": login_url,
                    "redirect_field_name": redirect_field_name,
                    "redirect_field_value": redirect_field_value})
        return ret

