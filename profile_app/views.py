# リダイレクト、ビュー
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.views.decorators.http import require_POST

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

# timeについて
import datetime
from django.utils import timezone

# EmployeeCreateView用（MySignUp）
from allauth.account.views import SignupView
from accounts.forms import MySignupForm

# ProfileInline
from django.urls import reverse_lazy
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from django.views.generic import TemplateView
from .models import Profile, Department

# Log用
import logging
logger = logging.getLogger(__name__)

def lastname(request):
    """共通画面用user_id,lastname"""
    user_id = -1
    is_staff = False
    try:
        logger.debug('ユーザー：{}'.format(request.user))
        data = Profile.objects.get(id_id__exact=request.user.id)
        user_id = Profile.objects.get(id_id__exact=request.user.id).user_id
        is_staff = request.user.is_staff
    except:
        logger.debug('profileにデータを登録していない')
        data = 'データ無し'
    return {'common_last_name': data ,'user_id': user_id, 'common_is_staff': is_staff
            ,'date_today': datetime.date.today()}


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
        profiles = Profile.objects.filter(delete=0).order_by('user_id')
        return profiles    


class EmployeeView(generic.DetailView, LoginRequiredMixin):
    """社員詳細画面"""
    model = Profile
    template_name = "ENP002_employee.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        birth = Profile.objects.get(user_id=self.kwargs['pk']).birth # pkを指定してデータを絞り込む
        time0 = int("".join(str(birth).split("-")))

        time = str(datetime.date.today())
        now_time = int("".join(time.split("-")))
        age = int(((now_time - time0) / 10000))+1
        context['count_age'] = age
        return context

@require_POST
def EmployeeDeleteView(request, pk):
    logger.debug("pk={}".format(pk))
    employee = get_object_or_404(CustomUser, id=pk) #データが存在していることを確認する
    profile = get_object_or_404(Profile, id_id=pk) #同上
    if employee and profile:
        logger.debug("ユーザーを削除している：　no.{} name.{}".format(pk, profile))
        if request.user.is_staff: # 管理者権限を確認する
            if request.user.id == pk:
                logger.info("自分のデータを削除できません。")
                messages.add_message(request, messages.ERROR, '自分のデータを削除できません。')
                return redirect(request.META['HTTP_REFERER'])
            else:
                CustomUser.objects.filter(id=pk).update(is_active = 0) #CustomUserの削除
                Profile.objects.filter(id_id=pk).update(delete = 1, update_date = timezone.now(),
                 update_id = request.user.id) #Profileの削除
        else:
            logger.info("管理者のみprofileを削除することができる")
            raise PermissionDenied # 権限なし

    response = redirect('profile_app:employee_list')
    return response

