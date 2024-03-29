from typing import Counter
from django.db.models.expressions import Value
from django.shortcuts import render
from django.urls.conf import path

# Create your views here.
from django.http import HttpResponse

from profile_app.models import EDepartment, EProfile
# モデル
from .models import EProduct,EAsset,EAssetHistory

# form
from .forms import ProductEditForm,AssetCreateForm,AssetHistoryCreateForm
# ログインを要求する用
from django.contrib.auth.mixins import LoginRequiredMixin
# メッセージ用
from django.contrib import messages
# リダイレクト、ビュー
from django.views import generic
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
# 404、500など
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

# Log用
import logging
logger = logging.getLogger(__name__)
# DB接続
from django.db import connection as c
cur = c.cursor()
import sys, os, psycopg2
# タイムゾーンを指定
from django.utils import timezone

import time
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.db.models import Max
from urllib.parse import urlencode

from datetime import datetime as dt

from django.http import JsonResponse
#const用
from asset_app import consts

# ページネーション用
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

#新しいimport方法
#import asset_app.forms as asset_form
def index(request):
    return HttpResponse("Hello.")

class ProductListView(generic.ListView):
    """品名一覧画面"""
    model = EProduct
    template_name = 'PRO001_product_list.html'
    context_object_name = 'product_list'
    paginate_by = 10
 
    def get_queryset(self):
        """取得するオブジェクトの一覧を動的に変更する"""
        self.request.session['update_pre_page'] = 'product_list'#セッション保存
        Products = EProduct.objects.filter(delete=0).order_by('product_id')
        return Products

class ProductCreateView(LoginRequiredMixin,generic.CreateView):
    """品名登録画面"""
    model = EProduct
    template_name = 'PRO002_product_create.html'
    form_class = ProductEditForm
    #success_url = reverse_lazy('asset_app:product_list')
    
    def get_success_url(self):
        return reverse_lazy('asset_app:product_list')

    def form_valid(self,form):
        """バリデーションがうまくいったとき"""
        messages.success(self.request,'品名を登録しました')
        product = form.save(commit=False)
        product.create_id = self.request.user.id
        product.update_id = self.request.user.id

        # formのデータ取得
        product_name_cleaned = self.request.POST['product_name']
        product_abbreviation_cleaned = self.request.POST['product_abbreviation']
        # 削除された部門が存在するか確認
        product_name_delete_exist = EProduct.objects.filter(product_name__exact = product_name_cleaned).filter(delete=1).exists()
        product_abbreviation_exist = EProduct.objects.filter(product_abbreviation__exact = product_abbreviation_cleaned).filter(delete=1).exists()
        
        if product_name_delete_exist and product_abbreviation_exist:
            product_name_delete = EProduct.objects.filter(delete=1).filter(product_name__exact = product_name_cleaned)
            # product_abbreviation_delete = EProduct.objects.filter(delete=1).filter(product_abbreviation__exact = product_abbreviation_cleaned)
            # 部門IDを扱う
            new_product_id = product_name_delete[0].product_id
            # update(delete=1)の部門
            EProduct.objects.filter(product_name__exact = product_name_cleaned).filter(product_abbreviation__exact = product_abbreviation_cleaned).filter(delete=1).update(
            product_id = new_product_id,
            delete = 0,
            update_date = timezone.now(),
            update_id = self.request.user.id,
            )
            return HttpResponseRedirect(self.get_success_url()) 
        
        return super().form_valid(form)

    def form_invalid(self,form):
        """バリデーションがうまくいかなかったとき"""
        messages.error(self.request,"品名の登録を失敗しました")
        return super().form_invalid(form)

def duplicate_product(request):
    """品名重複チェック"""
    #画面から入力した品名を取得する
    product_name = request.GET.get('product_name',None)
    response ={
        'exists_product_name':EProduct.objects.filter(product_name__iexact = product_name).filter(delete=0).exists()
    }
    return JsonResponse(response)

def duplicate_product_abbreviation(request):
    """略称重複チェック"""
    #画面から入力した略称を取得する
    product_abbreviation = request.GET.get('product_abbreviation',None)
    response ={
        'exists_product_abbreviation':EProduct.objects.filter(product_abbreviation__iexact = product_abbreviation).filter(delete=0).exists()
    }
    return JsonResponse(response)

def check_delete_product(request):
    """品名削除チェック"""
    #画面から入力した部門を取得する
    product_name = request.GET.get('product_name',None)
    response ={
        'delete_product_name':EProduct.objects.filter(product_name__iexact = product_name).filter(delete=1).exists()
    }
    return JsonResponse(response)

def check_delete_product_abbreviation(request):
    """略称削除チェック"""
    #画面から入力した部門を取得する
    product_abbreviation = request.GET.get('product_abbreviation',None)
    response ={
        'delete_product_abbreviation':EProduct.objects.filter(product_abbreviation__iexact = product_abbreviation).filter(delete=1).exists()
    }
    return JsonResponse(response)

class ProductUpdateView(LoginRequiredMixin,generic.UpdateView):
    """品名編集画面"""
    model = EProduct
    template_name = 'PRO003_product_update.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse_lazy('asset_app:product_list')
    
    def get_form_kwargs(self, *args, **kwargs):
        """viewからformにパラメータを渡す"""
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        return form_kwargs

    def form_valid(self,form):
        messages.success(self.request,"品名の登録しました")
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,"品名の登録を失敗しました")
        return super().form_invalid(form)

# @require_POST
# def ProductDeleteView(request, pk):
#     """
#     品名一覧画面の削除ボタンをクリックしたら品名を削除できる処理
#     """
#     # データが存在していることを確認する
#     product = get_object_or_404(EProduct, product_id=pk)
#     # productの削除
#     EProduct.objects.filter(product_id=pk).delete()
#     messages.add_message(request, messages.SUCCESS, 'データを削除しました。')
#     return redirect('asset_app:product_list')
@require_POST
def ProductDeleteView(request, pk):
    """品名削除"""
    logger.debug("pk={}".format(pk))
    #データが存在していることを確認する
    product = get_object_or_404(EProduct, product_id=pk)
    #該当品名に所属している資産の名数をcountする
    asset = EAsset.objects.filter(product_ass_id=pk).count()
    if product :
        if asset > 0:
            logger.info("品名のデータを削除できません。") 
            messages.add_message(request, messages.ERROR, '該当品名には資産が所属しているため、削除できません。')
            return redirect(request.META['HTTP_REFERER'])
        else:
            logger.info("これはelse")
            EProduct.objects.filter(product_id=pk).update(delete = 1)
            messages.add_message(request, messages.SUCCESS, '品名を削除しました。')

    response = redirect('asset_app:product_list')
    return response

class AssetListView(generic.ListView):
    """資産一覧画面"""
    model = EAsset
    template_name = 'ASS001_asset_list.html'
    context_object_name = 'asset_list'
    paginate_by = 10
    #ProductとAssetの結合
    queryset = EAsset.objects.select_related('product_ass_id')#prefetch_related('asset_ash_id')      
    
    def get_count_product(product_list_sql):
        """SQL文の実行"""
        cur.execute(product_list_sql)
        result = cur.fetchall()
        return result
    
    def get_count_asset(asset_list_sql):
        cur.execute(asset_list_sql)
        result = cur.fetchall()
        return result
    
    def get_context_data(self, **kwargs):
        """テンプレートへ渡す辞書を作成するメソッド"""
        # 品名の使用可能数、総数を取得するSQL文
        product_list_sql = '''
        SELECT
            EPT.PRODUCT_ID 
            , EPT.PRODUCT_NAME
            , COUNT(TEMP.STATUS < 3 OR NULL) AS AVAILABLE_CNT
            , COUNT(TEMP.STATUS < 5 OR NULL ) AS TOTAL_CNT
        FROM(
            SELECT
                EA.PRODUCT_ASS_ID
                , EAH.ASSET_ASH_ID
                , EAH.STATUS
                , EAH.UPDATE_DATE
            FROM
                E_ASSET_HISTORY EAH
                INNER JOIN E_ASSET EA
                ON EAH.ASSET_ASH_ID = EA.ASSET_ID
            WHERE
                EAH.UPDATE_DATE = (
                    SELECT
                        MAX(UPDATE_DATE)
                    FROM
                        E_ASSET_HISTORY AS EH
                    WHERE
                        EAH.ASSET_ASH_ID = EH.ASSET_ASH_ID
                )
            AND	 EAH.DELETE = 0
            AND	 EA.DELETE = 0
        ) TEMP
        INNER JOIN E_PRODUCT EPT
            ON TEMP.PRODUCT_ASS_ID = EPT.PRODUCT_ID
            AND EPT.DELETE = 0
        INNER JOIN E_ASSET EAT
            ON TEMP.ASSET_ASH_ID = EAT.ASSET_ID
            AND EAT.DELETE = 0
        GROUP BY
            EPT.PRODUCT_ID
        ORDER BY
            EPT.PRODUCT_ID DESC; '''
        # 資産の使用可能数、総数を取得するSQL文
        asset_list_sql ='''
        SELECT
            EPT.PRODUCT_ID 
            ,EA.MODEL_NAME
            ,COUNT(MD.STATUS < 3 OR NULL) AS AVAILABLE_CNT
            ,COUNT(MD.STATUS < 5 OR NULL) AS TOTAL_CNT
        FROM(
            SELECT
                EAT.PRODUCT_ASS_ID
                ,EAT.MODEL_NAME
                , EAH.ASSET_ASH_ID
                , EAH.STATUS
                , EAH.UPDATE_DATE
            FROM
                E_ASSET_HISTORY EAH
                INNER JOIN E_ASSET EAT
                ON EAH.ASSET_ASH_ID = EAT.ASSET_ID
            WHERE
                EAH.UPDATE_DATE = (
                    SELECT
                        MAX(UPDATE_DATE)
                    FROM
                        E_ASSET_HISTORY AS EH
                    WHERE
                        EAH.ASSET_ASH_ID = EH.ASSET_ASH_ID
                )
            AND  EAH.DELETE = 0
            AND  EAT.DELETE = 0
        ) MD
        INNER JOIN E_PRODUCT EPT
            ON MD.PRODUCT_ASS_ID = EPT.PRODUCT_ID
            AND  EPT.DELETE = 0
        INNER JOIN E_ASSET EA
            ON MD.ASSET_ASH_ID = EA.ASSET_ID
            AND MD.MODEL_NAME = EA.MODEL_NAME
            AND EA.DELETE = 0
        GROUP BY
            EPT.PRODUCT_ID,EA.MODEL_NAME
        ORDER BY
            EPT.PRODUCT_ID DESC,EA.MODEL_NAME DESC;'''
        product_list = AssetListView.get_count_product(product_list_sql)
        asset_list = AssetListView.get_count_asset(asset_list_sql)
        # 継承先のListViewのget_context_dataメソッドを実行し、それをcontext変数に代入しています。
        context = super(AssetListView, self).get_context_data(**kwargs)
        context.update({
            'product_list' : product_list,
            'asset_list' : asset_list,
        })
        # ページネーション
        paginator = Paginator(product_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj

        context['product_list'] = paginator.page(context['page_obj'].number)      
        return context

class AssetCreateView(LoginRequiredMixin,generic.CreateView):
    """資産登録画面"""
    model = EAsset
    template_name = 'ASS002_asset_create.html'
    form_class = AssetCreateForm
    #success_url = reverse_lazy('asset_app:asset_create_done')  
              
    def form_valid(self, form):
        """ 
        フォームを保存し、success_url を使用して 
        HttpResponseRedirect オブジェクトを返します
        """
        # リダイレクト先のパスを取得する
        redirect_url = reverse('asset_app:ASS003_asset_create_done')
        parameter = self.create_asset_object(self.request, form)
        # パラメータのdictをurlencodeする
        parameters = urlencode(parameter)
        # URLにパラメータを付与する
        url = f'{redirect_url}?{parameters}'       
        return redirect(url)

    def create_asset_object(self, request, form):
        """ オブジェクトを作成する機能 """        

        # DBから読み込み       
        product_abbreviation = EProduct.objects.get(product_id=form.cleaned_data['product_ass_id']).product_abbreviation
        #複数の入力フィールド値 取得
        serial_number_list = request.POST.getlist("serial_number")      
        #DBから同じ品物、日付の資産のnumの最大値を取得する
        max_serial_number = EAsset.objects.filter(asset_id__icontains = "ALIBER-"+product_abbreviation+"-"+str(form.cleaned_data['purchase_date'])).aggregate(Max('num'))['num__max']       
        #DBにmax_serial_numberが0ではない場合は+１、
        #0の場合は m=1
        if max_serial_number is not None :                
            m = max_serial_number+1
        else:
            m = 1
        
        #asset_id list
        asset_id_list = []
        #品名ID
        product_id = EProduct.objects.get(product_id__exact = form.cleaned_data['product_ass_id']).product_id

        #品名
        product_name = EProduct.objects.get(product_id__exact = form.cleaned_data['product_ass_id']).product_name
        #モデル名
        model_name_t = form.cleaned_data['model_name']
        #入庫日
        purchase_date_t = form.cleaned_data['purchase_date']
        
        #複数データ挿入
        for serial_number in serial_number_list:
            self.object = EAsset.objects.create(
                asset_id = "ALIBER-"+product_abbreviation+"-"+str(form.cleaned_data['purchase_date'])+"-"+str(m),
                model_name = model_name_t,
                storing_date = timezone.now(),
                purchase_date = purchase_date_t,
                serial_number = serial_number,
                delete = 0,
                create_date = timezone.now(),
                create_id = self.request.user.id,
                update_date = timezone.now(),
                update_id = self.request.user.id,
                product_ass_id = product_id,
                num = m,
            )
            asset_id_list.append("ALIBER-"+product_abbreviation+"-"+str(form.cleaned_data['purchase_date'])+"-"+str(m))            
            #データ挿入(asset_history)
            self.object = EAssetHistory.objects.create(
                asset_ash_id = "ALIBER-"+product_abbreviation+"-"+str(form.cleaned_data['purchase_date'])+"-"+str(m),
                status = 0,              
                delete = 0,
                create_date = timezone.now(),
                create_id = self.request.user.id,
                update_date = timezone.now(),
                update_id = self.request.user.id,                
            )
            m = m + 1
        results = {
            'product_name':product_name,
            'model_name_t':model_name_t,
            'purchase_date_t':purchase_date_t,
            'asset_id_list':asset_id_list,
            'serial_number_list':serial_number_list,
            }    
        return results

    def form_invalid(self,form):
        messages.error(self.request,"資産の登録を失敗しました")
        return super().form_invalid(form)

#     def post(self,request):
#         serial_number_list = self.request.POST.getlist("serial_number")
#         my_validation = check_val(serial_number_list)
#         return render(request,"ASS002_asset_create.html",my_validation)

# def check_val(serial_number_list):
#     my_validation = {}
#     if len(serial_number_list) > 10:
#         my_validation['error'] = "最大10個まで入力してください"
#     else:
#         my_validation['error'] =""
#     print("数字"+len(serial_number_list))
#     return my_validation

def create_done_view(request):
    #登録されたレコードの値を1つずつ取り出して辞書型変数contextに格納していきます。
    context = {
        'product_name' : request.GET.get('product_name'),
        'model_name_t' : request.GET.get('model_name_t'),
        'purchase_date_t' : dt.strptime(request.GET.get('purchase_date_t'),'%Y-%m-%d'),
        'asset_id_list' : eval(request.GET.get('asset_id_list')),
        'serial_number_list' : eval(request.GET.get('serial_number_list')),
    }
    # messagebox.showwarning('警告','生成した資産番号を必ずメモしてください')
    return render(request,'ASS003_asset_create_done.html',context) 

class AssetView(LoginRequiredMixin,generic.ListView):
    """資産詳細画面"""
    model = EAssetHistory
    template_name = "ASS004_asset.html"
    context_object_name = 'asset_detail_list'
    queryset = EAssetHistory.objects.select_related('asset_ash_id')
    paginate_by = 10

    def get_detail_asset(asset_detail_sql):
        """SQL文の実行"""
        cur.execute(asset_detail_sql)
        result = cur.fetchall()
        return result
    
    def get_context_data(self,**kwargs):
        #詳細画面の初期表示のSQL文
        asset_detail_sql = '''
        SELECT
            STS.PRODUCT_ASS_ID
            ,STS.ASSET_ASH_ID
            ,STS.SERIAL_NUMBER
            ,STS.MODEL_NAME
            ,STS.STORING_DATE
            ,STS.PURCHASE_DATE
            ,STS.VALUE
            ,STS.LAST_NAME
            ,STS.FIRST_NAME
            ,STS.REPAIR_REASON
            ,STS.PRODUCT_NAME
        FROM(
            SELECT
                EAT.PRODUCT_ASS_ID
                ,EAT.SERIAL_NUMBER
                ,EAT.MODEL_NAME
                ,EAT.STORING_DATE
                ,EAT.PURCHASE_DATE
                ,EAH.ASSET_ASH_ID
                ,M.VALUE
                ,EPE.LAST_NAME
                ,EPE.FIRST_NAME
                ,EAH.UPDATE_DATE
                ,EAH.REPAIR_REASON
                ,EPT.PRODUCT_NAME
            FROM
                E_ASSET_HISTORY EAH
            INNER JOIN
                E_ASSET EAT
                ON EAT.ASSET_ID = EAH.ASSET_ASH_ID
            INNER JOIN
                E_PRODUCT EPT
                ON EPT.PRODUCT_ID = EAT.PRODUCT_ASS_ID
            LEFT JOIN
                E_PROFILE EPE
                ON EPE.USER_ID = EAH.USER_ID
            INNER JOIN
                M_LIST M
                ON M.ID = EAH.STATUS
                AND CODE_TYPE = 2
            WHERE
                EAH.UPDATE_DATE = (
                    SELECT
                        MAX(UPDATE_DATE)
                    FROM
                        E_ASSET_HISTORY AS EH
                    WHERE
                        EAH.ASSET_ASH_ID = EH.ASSET_ASH_ID
                )
        )STS
        WHERE
            STS.PRODUCT_ASS_ID = :PARAM1 
            :PARAM2
        ORDER BY
            STS.PRODUCT_ASS_ID,STS.ASSET_ASH_ID; '''

        #１番目のパラメータ
        #product_idは使わなく、ｐｋを利用する
        pk = self.kwargs['pk']
        try:
            #２番目のパラメータが存在する場合
            model_name = self.kwargs['model_name']
            #二つのパラメータから遷移した場合のセッション保存
            self.request.session['parameter_product'] = pk
            self.request.session['parameter_model_name'] = model_name
        except:
            #２番目のパラメータが存在しない場合
            model_name = None
            #一つのパラメータから遷移した場合のセッション保存
            self.request.session['parameter_product'] = pk
            self.request.session['parameter_model_name'] = "" 


        if model_name is not None:
            #Sql文の動的条件（二つ）をリプレイスする
            asset_detail_sql = asset_detail_sql.replace(":PARAM1", str(pk)).replace(":PARAM2", " and sts.model_name = '" + model_name+ "'")
        else:
            #Sql文の動的条件（一つ目）をリプレイスする、二つ目のパラメータを空にリプレイスする
            asset_detail_sql = asset_detail_sql.replace(":PARAM1", str(pk)).replace(":PARAM2", "")
            
        # 継承先のListViewのget_context_dataメソッドを実行し、それをcontext変数に代入しています。
        asset_detail_list = AssetView.get_detail_asset(asset_detail_sql)
        context = super(AssetView, self).get_context_data(**kwargs)
        context.update({
            'asset_detail_list' : asset_detail_list,
            'form' : AssetHistoryCreateForm,
        })

        # ページネーション
        paginator = Paginator(asset_detail_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj

        context['asset_detail_list'] = paginator.page(context['page_obj'].number)      
        return context

def ajax_get_department(request):
    pk = request.GET.get('pk')
    profile_list = []
    # pkパラメータがない、もしくはpk=空文字列だった場合は全カテゴリを返しておく。
    if pk:
        # pkがあれば、そのpkでカテゴリを絞り込む
        profile_list = EProfile.objects.filter(department_pro_id=pk)

        # [ {'name': '営業部', 'pk': '1'}, {...}, {...} ] という感じのリストになる。
        profile_list = [{'pk': profile.pk, 'name': profile.last_name + ' ' +  profile.first_name} for profile in profile_list]

    # JSONで返す。
    return JsonResponse({'profileList': profile_list})

def post(request):
    """貸出ボタンクリックしてからのデータ保存方法"""

    #指定された資産番号の取得
    asset_id_hidden = request.POST.get("asset_id_hidden")
    #フォームに入力された値を辞書で返す
    profile = request.POST.get("profile")
    repair_reason = ""
    delete = 0
    #貸出済ボタンのokボタンをクリックした時のstatusの値の設定
    if 'lend' in request.POST:            
        status_t = consts.STATUS_LEND_OUT
    #返却済ボタンのokボタンをクリックしてた時のstatusの値の設定     
    elif 'return' in request.POST:
        status_t = consts.STATUS_RETURNED
    #修理依頼済ボタンのokボタンをクリックした時のstatusと修理理由の値の設定
    elif 'repair' in request.POST:
        repair_reason = request.POST.get("repair_reason")
        status_t = consts.STATUS_REPAIR_REQUESTED
    #修理済ボタンをクリックした時のstatusとprofileの値の設定
    elif 'btn_repair_done' in request.POST:
        profile = request.user.id
        status_t = consts.STATUS_REPAIRED
    #削除ボタンをクリックした時のdelete,statusとprofileの値の設定
    elif 'delete' in request.POST:
        delete = 1
        status_t = consts.STATUS_UNAVAILABLE
        profile = request.user.id
    else:
        print('lend以外')
        
    #データ挿入(asset_history)
    new_asset_history = EAssetHistory.objects.create(
        status = status_t,
        user_id = profile,
        repair_reason = repair_reason,               
        delete = delete,
        create_date = timezone.now(),
        create_id = request.user.id,
        update_date = timezone.now(),
        update_id = request.user.id,
        asset_ash_id = asset_id_hidden,
    )
    return redirect('asset_app:asset_list')

class AssetLifeCycleView(LoginRequiredMixin, generic.ListView):
    """資産ライフサイクル画面"""
    model = EAssetHistory
    template_name = "ASS005_asset_lifecycle.html"
    paginate_by = 10
    
    def get_asset_lifecycle(asset_lifecycle_sql):
        """SQL文の実行"""
        cur.execute(asset_lifecycle_sql)
        result = cur.fetchall()
        return result
    
    def get_context_data(self,**kwargs):
        #資産ライフサイクル画面の初期表示のSQL文
        asset_lifecycle_sql = '''
        SELECT
            EPT.PRODUCT_NAME
            ,EAT.MODEL_NAME
            ,EAH.ASSET_ASH_ID
            ,EAT.SERIAL_NUMBER
            ,EAH.UPDATE_DATE
            ,M.VALUE
            ,EPE.LAST_NAME
            ,EPE.FIRST_NAME
        FROM
            E_ASSET_HISTORY EAH
        INNER JOIN
            E_ASSET EAT
            ON EAH.ASSET_ASH_ID = EAT.ASSET_ID
        LEFT JOIN
            E_PROFILE EPE
            ON EPE.USER_ID = EAH.USER_ID
        INNER JOIN
            M_LIST M
            ON M.ID = EAH.STATUS
            AND CODE_TYPE = 2
        INNER JOIN
            E_PRODUCT EPT
            ON EAT.PRODUCT_ASS_ID = EPT.PRODUCT_ID
        WHERE
            EAH.ASSET_ASH_ID = ':parameter'
        ORDER BY
            EAH.UPDATE_DATE DESC;'''
        asset_id = self.kwargs['asset_id']
        asset_lifecycle_sql = asset_lifecycle_sql.replace(":parameter", asset_id)
        asset_lifecycle_list = AssetLifeCycleView.get_asset_lifecycle(asset_lifecycle_sql)
        context = super(AssetLifeCycleView, self).get_context_data(**kwargs)
        context.update({
            'asset_lifecycle_list' : asset_lifecycle_list,
        })
        # ページネーション
        paginator = Paginator(asset_lifecycle_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        context['page_obj'] = page_obj

        context['asset_lifecycle_list'] = paginator.page(context['page_obj'].number)
      
        return context

def form_save(request, form, messages_success):
    Product = form.save(commit=False)
    Product.user = request.user
    Product.save()
    messages.success(request, messages_success)
    return form
