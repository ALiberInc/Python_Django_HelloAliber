# リダイレクト、ビュー
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse

# モデル
from .models import *
from accounts.models import CustomUser

# form
from .forms import *

# メッセージ用
from django.contrib import messages

# ログインを要求する用
from django.contrib.auth.mixins import LoginRequiredMixin

# 404、500など
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from datetime import timedelta

# EmployeeCreateView用（MySignUp）
from allauth.account.views import SignupView
from accounts.forms import MySignupForm

# ProfileInline
from django.urls import reverse_lazy
from extra_views import InlineFormSetFactory, CreateWithInlinesView,UpdateWithInlinesView
from django.views.generic import TemplateView
from .models import Profile, Department

# from extra_views import InlineFormSet, UpdateWithInlinesView
from django.http.response import HttpResponse
from django.shortcuts import render
from . import forms
from django.template.context_processors import csrf
# Log用
import logging
logger = logging.getLogger(__name__)

def lastname(request):
    """共通画面用user_id,lastname"""
    try:
        logger.debug('ユーザー：{}'.format(request.user))
        data = Profile.objects.get(id_id__exact=request.user.id)
        user_id = Profile.objects.get(id_id__exact=request.user.id).user_id
    except:
        logger.debug('profileにデータを登録していない')
        data = 'データ無し'
        user_id = -1
    return {'common_last_name': data ,'user_id': user_id}


class IndexView(generic.TemplateView):
    """（仮）HP"""
    template_name = "index.html"


class EmployeeListView(generic.ListView):
    """社員一覧画面"""
    model = Profile
    template_name = "ENP001_employee_list.html"
    context_object_name = 'member_list'
    paginate_by = 6

    def get_queryset(self):
        profiles = Profile.objects.order_by('user_id')
        return profiles


class EmployeeView(generic.DetailView, LoginRequiredMixin):
    """社員詳細画面"""
    model = Profile
    template_name = "ENP002_employee.html"


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    """社員編集"""
    model = Profile
    template_name = 'ENP004_employee_update.html'
    form_class = ProfileEditForm
    
    def get_success_url(self):
        return reverse_lazy('profile_app:employee', kwargs={'pk':self.kwargs['pk']})
    
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        
        gender_value = Profile.objects.get(user_id__exact=self.kwargs['pk']).gender
        email_value = CustomUser.objects.get(id__exact=self.kwargs['pk']).email
        form_kwargs['initial'] = {
            'email' : email_value,
            'gender' : gender_value
        }
        # form_class = ProfileEditForm(initial={'email':'1'})
        return form_kwargs

    
    def form_valid(self, form):
        # 元々のソース
        form = form_save(self.request,form, 'プロフィール更新しました。')
        email_cleaned =self.request.POST['email']
        logger.debug("メールアドレス:{}".format(self.request.POST['email']))
        customeruser_id = Profile.objects.get(user_id__exact=self.kwargs['pk']).id_id
        CustomUser.objects.filter(id=customeruser_id).update(email = email_cleaned)
        gender_cleaned = self.request.POST['gender']#formのデータ取得
        logger.debug("gender:{}".format(gender_cleaned))
        # gender_id = Profile.objects.get(user_id__exact=self.kwargs['pk']).gender#DBの一列がらデータ探す
        # logger.debug("GG:{}".format(gender_id))
        # Profile.objects.filter(user_id=1).update(gender = gender_cleaned)#更新
        gender_save= form.save(commit=False)
        gender_save.gender = gender_cleaned

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新が失敗しました。")
        return super().form_invalid(form)
   

def form_save(request, form, messages_success):
    profile = form.save(commit=False)
    profile.user = request.user
    profile.save()
    messages.success(request, messages_success)
    return form

