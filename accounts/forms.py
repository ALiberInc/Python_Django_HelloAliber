from __future__ import absolute_import
from allauth.account.forms import ResetPasswordForm,\
    EmailAwarePasswordResetTokenGenerator

from .models import CustomUser
from profile_app.models import Profile, Department
import random, string
import logging

logger = logging.getLogger(__name__)

# リライトResetPasswordForm
# リライトclean_email
from allauth.account.utils import (
    filter_users_by_email,
)

# リライトsave
from django import forms
from django.urls import reverse

from allauth.utils import build_absolute_uri, set_form_field_order
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import (
    user_pk_to_url_str,
    setup_user_email,
    user_username,
    user_email,
    get_user_model,
)

# リライトSignupForm
from allauth.account.forms import BaseSignupForm

default_token_generator = EmailAwarePasswordResetTokenGenerator()

# リライトLoginForm
from allauth.account.forms import LoginForm
from django.utils.translation import gettext, gettext_lazy as _, pgettext

class MyResetPasswordForm(ResetPasswordForm):
    last_name = forms.CharField(label='姓', required=True, )
    first_name = forms.CharField(label='名', required=True, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['maxlength'] = '30'
        self.fields['email'].error_messages = {
            'required': 'メールアドレスを入力してください。',
            'maxlength':'15桁以内を入力してください。'}
        self.fields['last_name'].widget.attrs['maxlength'] = '15'
        self.fields['last_name'].widget.attrs['placeholder'] = '田中'
        self.fields['last_name'].error_messages = {
            'required': '姓を入力してください。',
            'maxlength':'15桁以内を入力してください。'}
        self.fields['first_name'].widget.attrs['maxlength'] = '15'
        self.fields['first_name'].widget.attrs['placeholder'] = '太郎'
        self.fields['first_name'].error_messages = {
            'required': '名を入力してください。',
            'maxlength':'15桁以内を入力してください。'}

    # リライト
    def clean_email(self):
        email = self.data.get('email')
        if len(email) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        return self.cleaned_data["email"]

    def clean_last_name(self):
        last_name = self.data.get('last_name')
        if len(last_name) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["last_name"]

    def clean_first_name(self):
        first_name = self.data.get('first_name')
        if len(first_name) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["first_name"]
    
    def clean(self):
            email = self.cleaned_data.get('email')
            last_name = self.cleaned_data.get('last_name')
            first_name = self.cleaned_data.get('first_name')
            self.users = filter_users_by_email(email, is_active=True)
            users = CustomUser.objects.filter(email__iexact=email, is_active=True).first()
            if email == None:
                raise forms.ValidationError("")
            if users:
                if users.last_name != last_name or users.first_name != first_name:
                    raise forms.ValidationError("該当するアカウントが見つかりません。")
            else:
                raise forms.ValidationError("該当するアカウントが見つかりません。")

    # リライト
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        last_name = self.data.get('last_name')
        token_generator = kwargs.get("token_generator",
                                     default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse("account_reset_password_from_key",
                           kwargs=dict(uidb36=user_pk_to_url_str(user),
                                       key=temp_key))
            url = build_absolute_uri(
                request, path)

            context = {
                "last_name": last_name,
                "password_reset_url": url,
            }

            if app_settings.AUTHENTICATION_METHOD \
                    != 'email':
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key',
                email,
                context)
        return self.cleaned_data["email"]


def GetRandomStr(num):
    # 英数字をすべて取得
    dat = string.digits + string.ascii_lowercase + string.ascii_uppercase
    return ''.join([random.choice(dat) for i in range(num)])


class MySignupForm(BaseSignupForm):
    """社員新規form 元登録form"""
    # パスワード生成用（5桁ランダムテキスト）
    random_password = ""
    department_pro = forms.ModelChoiceField(Department.objects, label='部門', initial=0)

    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'] = forms.CharField(label='password', initial=GetRandomStr(5), )
        self.fields['password1'].widget = forms.HiddenInput()
        self.fields['last_name'] = forms.CharField(label='姓', )
        self.fields['last_name'].widget.attrs['maxlength'] = '15'
        self.fields['last_name'].help_text = '15桁以下を入力してください。'
        self.fields['last_name'].error_messages = {
            'required': '姓を入力してください。',
            'maxlength':'15桁以内を入力してください。'}
        self.fields['first_name'] = forms.CharField(label="名", )
        self.fields['first_name'].widget.attrs['maxlength'] = '15'
        self.fields['first_name'].help_text = '15桁以下を入力してください。'
        self.fields['first_name'].error_messages = {
            'required': '名を入力してください。',
            'maxlength':'15桁以内を入力してください。'}
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['email'].widget.attrs['maxlength'] = '30'
        self.fields['email'].error_messages = {
            'required': 'メールアドレスを入力してください。',
            'maxlength':'30桁以内を入力してください。'}
        if hasattr(self, 'field_order'):
            set_form_field_order(self, self.field_order)

    field_order = [
        "last_name", "first_name", "email", "department_pro"
    ]

    def clean_last_name(self):
        last_name = self.data.get('last_name')
        if len(last_name) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["last_name"]

    def clean_first_name(self):
        first_name = self.data.get('first_name')
        if len(first_name) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["first_name"]

    def clean_email(self):
        email = self.data.get('email')
        if len(email) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        return self.cleaned_data["email"]

    def clean(self):
        super(MySignupForm, self).clean()

        # `password` cannot be of type `SetPasswordField`, as we don't
        # have a `User` yet. So, let's populate a dummy user to be used
        # for password validaton.
        dummy_user = get_user_model()
        user_username(dummy_user, self.cleaned_data.get("username"))
        user_email(dummy_user, self.cleaned_data.get("email"))
        password = self.cleaned_data.get('password1')
        logger.debug("新しいパスワード確認：{}".format(password))
        self.random_password = password

        if password:
            try:
                get_adapter().clean_password(
                    password,
                    user=dummy_user)
            except forms.ValidationError as e:
                self.add_error('email', e)
                # パスワードfieldが自動生成するので、エラーを出力しないはず

        return self.cleaned_data

    def save(self, request):
        request.password = self.random_password
        request.last_name = self.data.get('last_name')
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)

        # add password
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        
        return user

class MyLoginForm(LoginForm):
    """元LoginFormの入力チェックとエラーメッセージを修正する"""
    error_messages = {
        'account_inactive':
        ("該当アカウント現在使われておりません。"),

        'email_password_mismatch':
        ("メールアドレスまたはパスワードが間違っています。"),
    }

    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['maxlength'] = '30'
        self.fields['login'].error_messages = {
            'required': 'メールアドレスを入力してください。',
            'maxlength':'30桁以内を入力してください。'}
        self.fields['password'].widget.attrs['maxlength'] = '30'
        self.fields['password'].error_messages = {
            'required': 'パスワードを入力してください。',
            'maxlength':'30桁以内を入力してください。'}

    def clean_login(self):
        email = self.data.get('login')
        if len(email) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        return self.cleaned_data["login"]

    
    def clean_password(self):
        my_password = self.data.get('password')
        if len(my_password) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        return self.cleaned_data["password"]
    