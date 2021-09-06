from allauth.account.views import ConfirmEmailView, LoginView
from allauth.account import app_settings
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone

from django.db import connection as c
cur = c.cursor()

# MySignupView用：
from accounts.forms import MySignupForm
from accounts.models import CustomUser
from profile_app.models import EProfile,EDepartment

from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from allauth.account.views import CloseableSignupMixin, AjaxCapableProcessFormViewMixin, sensitive_post_parameters_m
from allauth.utils import get_form_class, get_request_param
from allauth.account.utils import (
    complete_signup,
    get_next_redirect_url,
    passthrough_next_redirect_url,
)
from allauth.exceptions import ImmediateHttpResponse

import logging
logger = logging.getLogger(__name__)

from accounts.forms import MyResetPasswordForm

class MyLoginView(LoginView):
    def form_valid(self, form):
        success_url = self.get_success_url()
        try:
            #session処理
            username = form.cleaned_data['login']
            logger.debug("user account={}".format(username))
            sql_select_userinfo = """
                SELECT
                    u.id,
                    u.is_staff,
                    p.id,
                    p.last_name
                FROM
                    accounts_customuser u
                INNER JOIN
                    e_profile p
                ON
                    u.id = p.user_id
                    and u.email = '{}'
                    and u.is_active = true
                    and p.delete = 0
                ;
            """.format(username)
            cur.execute(sql_select_userinfo)
            result = cur.fetchone()
            """@old
            user_id = CustomUser.objects.get(email__exact=username).id
            is_staff = CustomUser.objects.get(email__exact=username).is_staff
            id = EProfile.objects.get(user_id__exact=user_id).id
            last_name = EProfile.objects.get(user_id__exact=user_id).last_name
            self.request.session['last_name'] = last_name
            self.request.session['id'] = id
            self.request.session['user_id'] = user_id
            self.request.session['is_staff'] = is_staff
            """
            logger.debug("新しいセッション：" + str(result))
            self.request.session['user_id'] = result[0]
            self.request.session['is_staff'] = result[1]
            self.request.session['id'] = result[2]
            self.request.session['last_name'] = result[3]

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
        new_profile = EProfile.objects.create(
            user_id = CustomUser.objects.get(email = form.cleaned_data['email']).id,
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
            department_pro_id = EDepartment.objects.get(department = form.cleaned_data['department_pro']).dep_id,
            emergency_contact_1_name = blank,
            emergency_contact_1_relationship = blank,
            emergency_contact_1_phone = blank,
            emergency_contact_2_name = blank,
            emergency_contact_2_relationship = blank,
            emergency_contact_2_phone = blank,
            emergency_contact_3_name = blank,
            emergency_contact_3_relationship = blank,
            emergency_contact_3_phone = blank,
            create_date = timezone.now(),
            create_id = self.request.user.id,#ログインしているユーザーID
            update_date = timezone.now(),
            update_id = self.request.user.id,
            delete = 0,)

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


class MyPasswordResetView(AjaxCapableProcessFormViewMixin, FormView):
    template_name = "account/password_reset." + app_settings.TEMPLATE_EXTENSION
    form_class = MyResetPasswordForm
    success_url = reverse_lazy("account_reset_password_done")
    redirect_field_name = "next"

    def get_form_class(self):
        return get_form_class(app_settings.FORMS,
                              'reset_password',
                              self.form_class)

    def form_valid(self, form):
        form.save(self.request)
        messages.success(self.request,'パスワードリセット用のメールを送信しました。')
        return super(MyPasswordResetView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ret = super(MyPasswordResetView, self).get_context_data(**kwargs)
        login_url = passthrough_next_redirect_url(self.request,
                                                  reverse("account_login"),
                                                  self.redirect_field_name)
        # NOTE: For backwards compatibility
        ret['password_reset_form'] = ret.get('form')
        # (end NOTE)
        ret.update({"login_url": login_url})
        return ret
