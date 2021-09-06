# リダイレクト、ビュー
from django.http import response
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from django.db import connection as c
cur = c.cursor()

# モデル
from .models import EProfile, EDepartment
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
JST = datetime.timezone(datetime.timedelta(hours=9), "JST")

from django.http.response import JsonResponse
# タイムゾーンを指定
from django.utils import timezone

from django.http import HttpResponseRedirect

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
    except Exception as e:
        logger.debug(e)
        logger.debug('profileにデータを登録していない')
        last_name = 'データ無し'
    return {'common_last_name': last_name ,'user_id': user_id, 'common_is_staff': is_staff
            ,'date_today': datetime.date.today()}


class EmployeeListView(generic.ListView):
    """社員一覧画面"""
    model = EProfile
    template_name = "ENP001_employee_list.html"
    context_object_name = 'member_list'
    paginate_by = 10
                         
    def get_queryset(self):
        self.request.session['update_pre_page'] = "employee_list"#セッション保存
        sql_select_profiles = """
            SELECT
                p.id
                ,p.last_name
                ,p.first_name
                ,d.department
                ,p.last_name_k
                ,p.update_date
                ,u.is_staff
                ,u.is_active
                ,u.id
            FROM
                e_profile p
            INNER JOIN
                e_department d
            ON
                p.department_pro_id = d.dep_id
                AND d.delete = 0
            INNER JOIN
                accounts_customuser u
            ON
                p.user_id = u.id
            WHERE p.delete = 0
            ORDER BY p.user_id
            ;
        """
        cur.execute(sql_select_profiles)
        result = cur.fetchall()
        c.close()
        return result   

class EmployeeView(generic.DetailView, LoginRequiredMixin):
    """社員詳細画面"""
    model = EProfile
    template_name = "ENP002_employee.html"
    
    def get_context_data(self, **kwargs):
        self.request.session['update_pre_page'] = "employee"#セッション保存
        context = super().get_context_data(**kwargs)
        # データ追加（年齢、メールアドレス、部門、権限、アクティブ）
        sql_select_profile = """
            SELECT
                p.birth
                ,d.department
                ,u.email
                ,u.is_staff
                ,u.is_active
            FROM
                e_profile p
            INNER JOIN
                accounts_customuser u
            ON
                p.user_id = u.id
                AND p.id = {}
                AND p.delete = 0
            INNER JOIN
                e_department d
            ON
                p.department_pro_id = d.dep_id
                AND d.delete = 0
        """.format(self.kwargs['pk'])
        cur.execute(sql_select_profile)
        profile = cur.fetchone()
        c.close()
        #年齢算出：
        birth = profile[0]
        logger.debug("birth:" + str(birth))
        age = int((datetime.datetime.now(JST)-birth).days/365.25)
        logger.debug(str(age) + "才")
        context.update({
            'c_count_age':age,
            'c_department':profile[1],
            'c_email':profile[2],
            'c_is_staff':profile[3],
            'c_is_active':profile[4],
            })
        return context

@require_POST
def EmployeeDeleteView(request, id, user_id):
    """社員削除"""
    try:
        logger.debug("ユーザーを削除している：　id.{}, user_id.{}".format(id, user_id))
        # 管理者権限を確認する
        if request.user.is_staff:
            # 自分のデータを削除チェック
            if request.session['id'] == id:
                logger.info("自分のデータを削除できません。")
                messages.add_message(request, messages.ERROR, '自分のデータを削除できません。')
                return redirect(request.META['HTTP_REFERER'])
            else:
                sql_delete_employee = """
                    DELETE FROM e_profile	
                    WHERE id={id}	
                    ;
                    DELETE FROM account_emailaddress	
                    WHERE id={user_id}
                    ;
                    DELETE FROM accounts_customuser	
                    WHERE id={user_id}
                    ;
                """.format(id=id, user_id=user_id)
                cur.execute(sql_delete_employee)
                c.close()
                #EProfile.objects.filter(id=id).delete()
                #CustomUser.objects.filter(id=user_id).delete() #CustomUserの削除
                messages.add_message(request, messages.SUCCESS, 'データを削除しました。')
        else:
            logger.info("管理者のみprofileを削除することができる")
            raise PermissionDenied # 権限なし
        #次画面（employee_list）に遷移する
        response = redirect('profile_app:employee_list')
        return response
    except Exception as e:
        logger.error(e)
        response = redirect('profile_app:500')
        return response

@require_POST
def EmployeeSetActiveView(request, pk):
    """社員一覧画面　「アクティブにする」ボタン"""
    logger.debug("pk={}".format(pk))
    employee = get_object_or_404(CustomUser, id=pk) #データが存在していることを確認する
    profile = get_object_or_404(EProfile, user_id=pk) #同上
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
    profile = get_object_or_404(EProfile, user_id=pk) #同上
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
    model = EProfile
    template_name = 'ENP004_employee_update.html'
    form_class = ProfileEditForm
    
    def get_success_url(self):
        return reverse_lazy('profile_app:employee', kwargs={'pk':self.kwargs['pk']})
    
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        
        # DBから読み込み
        sql_select_user = """
            SELECT
                p.gender
                ,p.birth
                ,p.user_id
                ,p.department_pro_id
                ,u.email
                ,u.is_active
            FROM
                e_profile p
            INNER JOIN
                accounts_customuser u
            ON
                u.id = p.user_id
                AND p.id = {}
                AND p.delete = 0
            ;
        """.format(self.kwargs['pk'])
        cur.execute(sql_select_user)
        profile = cur.fetchone()
        c.close()
        birth = profile[1].strftime("%Y%m%d")
        form_kwargs['initial'] = {
            'gender' : profile[0],
            'birth' : birth,
            'id' : profile[2],
            'department_pro' : profile[3],
            'email' : profile[4],
            'is_active' : profile[5],
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
        customeruser_id = EProfile.objects.get(id__exact=self.kwargs['pk']).user_id
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

class DepartmentListView(generic.ListView):
    """部門一覧画面"""
    model = Department
    template_name = 'DEP001_department_list.html'
    context_object_name = 'department_list'
    paginate_by = 10
 
    def get_queryset(self):
        """取得するオブジェクトの一覧を動的に変更する"""
        self.request.session['update_pre_page'] = 'department_list'#セッション保存
        departments = Department.objects.filter(delete=0).order_by('dep_id')
        return departments

@require_POST
def DepartmentDeleteView(request, pk):
    """部門削除"""
    logger.debug("pk={}".format(pk))
    #データが存在していることを確認する
    department = get_object_or_404(Department, dep_id=pk)
    #該当部門に所属している社員の名数をcountする
    profile = Profile.objects.filter(department_pro_id=pk).count()
    if department :
        if profile > 0:
            logger.info("部門のデータを削除できません。") 
            messages.add_message(request, messages.ERROR, '該当部門には社員が所属しているため、削除できません。')
            return redirect(request.META['HTTP_REFERER'])
        else:
            logger.info("これはelse")
            Department.objects.filter(dep_id=pk).update(delete = 1)
            messages.add_message(request, messages.SUCCESS, '部門を削除しました。')

    response = redirect('profile_app:department_list')
    return response

class DepartmentCreateView(LoginRequiredMixin,generic.CreateView):
    """部門登録画面"""
    model = Department
    template_name = 'DEP002_department_create.html'
    form_class = DepartmentEditForm
    success_url = reverse_lazy('profile_app:department_list')
 
    def get_success_url(self):
        return reverse_lazy('profile_app:department_list')

    def form_valid(self,form):
        """バリデーションがうまくいったとき"""
        messages.success(self.request,'部門を登録しました')
        department = form.save(commit=False)
        department.create_id = self.request.user.id
        department.update_id = self.request.user.id       
        # formのデータ取得
        department_cleaned = self.request.POST['department']
        # 削除された部門が存在するか確認
        department_delete_exist = Department.objects.filter(department__exact = department_cleaned).filter(delete=1).exists()
        
        if department_delete_exist:
            department_delete = Department.objects.filter(delete=1).filter(department__exact = department_cleaned)
            # 部門IDを扱う
            value = department_delete[0].dep_id
            # update(delete=1)の部門
            Department.objects.filter(department__exact = department_cleaned).filter(delete=1).update(
            dep_id = value,
            establish_date = self.request.POST['establish_date'],
            delete = 0,
            update_date = timezone.now(),
            update_id = self.request.user.id,
            )
            return HttpResponseRedirect(self.get_success_url())     
            
        return super().form_valid(form)

    def form_invalid(self,form):
        """バリデーションがうまくいかなかったとき"""
        messages.error(self.request,"部門の登録が失敗しました")
        return super().form_invalid(form)

def validate_department(request):
    """重複チェック"""
    #画面から入力した部門を取得する
    department = request.GET.get('department',None)
    response ={
        'exists_department':Department.objects.filter(department__iexact = department).filter(delete=0).exists()
    }
    return JsonResponse(response)

def check_delete_department(request):
    """削除チェック"""
    #画面から入力した部門を取得する
    department = request.GET.get('department',None)
    response ={
        'delete_department':Department.objects.filter(department__iexact = department).filter(delete=1).exists()
    }
    return JsonResponse(response)

class DepartmentUpdateView(LoginRequiredMixin,generic.UpdateView):
    """部門編集画面"""
    model = Department
    template_name = 'DEP003_department_update.html'
    form_class = DepartmentEditForm

    def get_success_url(self):
        return reverse_lazy('profile_app:department_list')
    
    def get_form_kwargs(self, *args, **kwargs):
        """viewからformにパラメータを渡す"""
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        return form_kwargs

    def form_valid(self,form):
        messages.success(self.request,"部門の登録しました")
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,"部門の登録が失敗しました")
        return super().form_invalid(form)

class Test500View(generic.TemplateView):
    def index(self):
        try:
            test500 = EProfile.objects.get(id=-1)
        except :
            raise Exception


def form_save(request, form, messages_success):
    profile = form.save(commit=False)
    profile.user = request.user
    profile.save()
    messages.success(request, messages_success)
    return form
