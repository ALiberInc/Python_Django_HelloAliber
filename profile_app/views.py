# リダイレクト、ビュー
from django.urls import reverse_lazy
from django.views import generic

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
# from extra_views import CreateWithInlinesView, InlineFormSet

# ProfileInline
from django.urls import reverse_lazy
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import TemplateView
# from .forms import MySignupForm
from .models import Profile, Department

# Log用
import logging
logger = logging.getLogger(__name__)


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


class EmployeeView(generic.ListView, LoginRequiredMixin):
    """社員詳細画面"""
    model = Profile
    template_name = "ENP002_employee.html"
    context_object_name = 'member_list'

    def get_queryset(self):
        logger.info('ユーザー：{}'.format(self.request.user))
        profiles = Profile.objects.filter(id=self.request.user.id).first()

        return profiles

class EmployeeView2(generic.DetailView, LoginRequiredMixin):
    """社員詳細画面"""
    model = Profile
    template_name = "ENP002_employee.html"
    context_object_name = 'member_list'

    def get_queryset(self):
        logger.info('ユーザー：{}'.format(self.request.user))
        profiles = Profile.objects.filter(id=self.request.user.id).first()

        return profiles

