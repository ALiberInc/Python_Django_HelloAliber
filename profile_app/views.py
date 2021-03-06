# リダイレクト、ビュー
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

# モデル
from .models import *
from accounts.models import CustomUser
from allauth.account.models import EmailAddress

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

# ProfileInline
from django.urls import reverse_lazy
from .models import Profile, Department

# Log用
import logging
logger = logging.getLogger(__name__)


def lastname(request):
    """共通画面用user_id,lastname"""
    #指摘：セッションに保存する
    user_id = -1
    is_staff = False
    try:        
        logger.debug('ユーザー：{}'.format(request.user))
        last_name = request.session['last_name']
        user_id = request.session['user_id']
        is_staff = request.session['is_staff']
    except:
        logger.debug('profileにデータを登録していない')
        last_name = 'データ無し'
    return {'common_last_name': last_name ,'user_id': user_id, 'common_is_staff': is_staff
            ,'date_today': datetime.date.today()}


class EmployeeListView(generic.ListView):
    """社員一覧画面"""
    model = Profile
    template_name = "ENP001_employee_list.html"
    context_object_name = 'member_list'
    paginate_by = 10
                         
    def get_queryset(self):
        self.request.session['update_pre_page'] = "employee_list"#セッション保存
        profiles = Profile.objects.order_by('user_id')
        return profiles   

class EmployeeView(generic.DetailView, LoginRequiredMixin):
    """社員詳細画面"""
    model = Profile
    template_name = "ENP002_employee.html"
    
    def get_context_data(self, **kwargs):
        self.request.session['update_pre_page'] = "employee"#セッション保存
        context = super().get_context_data(**kwargs)
        
        #年齢算出：
        birth = Profile.objects.get(user_id=self.kwargs['pk']).birth # pkを指定してデータを絞り込む
        time0 = int("".join(str(birth).split("-")))

        time = str(datetime.date.today())
        now_time = int("".join(time.split("-")))
        age = int(((now_time - time0) / 10000))
        context['count_age'] = age
        return context

@require_POST
def EmployeeDeleteView(request, pk):
    """社員一覧画面　「非アクティブにする」ボタン"""
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
                Profile.objects.filter(id_id=pk).delete()
                CustomUser.objects.filter(id=pk).delete() #CustomUserの削除
                messages.add_message(request, messages.SUCCESS, 'データを削除しました。')
        else:
            logger.info("管理者のみprofileを削除することができる")
            raise PermissionDenied # 権限なし

    #次画面（employee_list）に遷移する
    response = redirect('profile_app:employee_list')
    return response


@require_POST
def EmployeeSetActiveView(request, pk):
    """社員一覧画面　「アクティブにする」ボタン"""
    logger.debug("pk={}".format(pk))
    employee = get_object_or_404(CustomUser, id=pk) #データが存在していることを確認する
    profile = get_object_or_404(Profile, id_id=pk) #同上
    if employee and profile:
        CustomUser.objects.filter(id=pk).update(is_active = 1) #CustomUserアクティブ化
        messages.add_message(request, messages.SUCCESS, 'アクティブにしました。')
    else:
        logger.info("管理者のみアクティブにすることができる")
        raise PermissionDenied # 権限なし

    response = redirect('profile_app:employee_list')
    return response


@require_POST
def EmployeeSetInActiveView(request, pk):
    """社員一覧画面　「非アクティブにする」ボタン"""
    logger.debug("pk={}".format(pk))
    employee = get_object_or_404(CustomUser, id=pk) #データが存在していることを確認する
    profile = get_object_or_404(Profile, id_id=pk) #同上
    if employee and profile:
        if request.user.id == pk:
            logger.info("自分のデータを非アクティブにする！")
            messages.add_message(request, messages.ERROR, '自分のデータを非アクティブにすることができません。')
            return redirect(request.META['HTTP_REFERER'])
        else:
            CustomUser.objects.filter(id=pk).update(is_active = 0) #CustomUser非アクティブ化
            messages.add_message(request, messages.ERROR, '非アクティブにしました。')
    else:
        logger.info("管理者のみ非アクティブにすることができる")
        raise PermissionDenied # 権限なし

    response = redirect('profile_app:employee_list')
    return response


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    """社員編集"""
    model = Profile
    template_name = 'ENP004_employee_update.html'
    form_class = ProfileEditForm
    
    def get_success_url(self):
        return reverse_lazy('profile_app:employee', kwargs={'pk':self.kwargs['pk']})
    
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        
        # DBから読み込み
        gender_value = Profile.objects.get(user_id__exact=self.kwargs['pk']).gender
        birth_value = Profile.objects.get(user_id__exact=self.kwargs['pk']).birth
        birth_value_c = birth_value.strftime("%Y%m%d")
        id_value = Profile.objects.get(user_id__exact=self.kwargs['pk']).id_id
        email_value = CustomUser.objects.get(id__exact=id_value).email
        is_active_value = CustomUser.objects.get(id__exact=id_value).is_active
        # Form初期値を設定する
        form_kwargs['initial'] = {
            'email' : email_value,
            'gender' : gender_value,
            'birth' : birth_value_c,
            'id' : id_value,
            'is_active' : is_active_value,
        }
        return form_kwargs
    
    def form_valid(self, form):
        form = form_save(self.request,form, 'プロフィール更新しました。')
        # formのデータ取得
        email_cleaned = self.request.POST['email']
        logger.debug("メールアドレス:{}".format(self.request.POST['email']))
        first_name_cleaned = self.request.POST['first_name']
        last_name_cleaned = self.request.POST['last_name']
        # email取得して、@を基準に１回割りして、@前の部分をusernameにする
        user_split = email_cleaned.split("@", 1)
        customeruser_id = Profile.objects.get(user_id__exact=self.kwargs['pk']).id_id
        is_active_cleaned = self.request.POST['is_active']

        # DB登録
        # table CustomUser
        CustomUser.objects.filter(id=customeruser_id).update(
            email = email_cleaned,
            is_active = is_active_cleaned,
            first_name = first_name_cleaned,
            last_name = last_name_cleaned,
            username = user_split[0],
        )
        # table EmailAddress
        EmailAddress.objects.filter(id=customeruser_id).update(
            email = email_cleaned,
        ) 
        gender_cleaned = self.request.POST['gender']
        birth_cleaned = datetime.datetime.strptime(self.request.POST['birth'], "%Y%m%d")
        profile = form.save(commit=False)
        profile.gender = gender_cleaned
        profile.birth = birth_cleaned
        profile.update_id = self.request.user.id#ログインしているユーザーID
        
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "更新が失敗しました。")
        return super().form_invalid(form)


class Test500View(generic.TemplateView):
    def index(self):
        try:
            test500 = Profile.objects.get(id=-1)
        except :
            raise Exception


def form_save(request, form, messages_success):
    profile = form.save(commit=False)
    profile.user = request.user
    profile.save()
    messages.success(request, messages_success)
    return form
