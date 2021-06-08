from typing import Counter
from django.shortcuts import render
from django.urls.conf import path
from django.views import generic
# Create your views here.
from django.http import HttpResponse
# モデル
from .models import Product,Asset,Asset_History
from django.urls import reverse_lazy
# form
from .forms import ProductEditForm,AssetCreateForm
# ログインを要求する用
from django.contrib.auth.mixins import LoginRequiredMixin
# メッセージ用
from django.contrib import messages
# 削除機能用
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
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

def index(request):
    return HttpResponse("Hello.")

class ProductListView(generic.ListView):
    """品名一覧画面"""
    model = Product
    template_name = 'PRO001_product_list.html'
    context_object_name = 'product_list'
    paginate_by = 10
 
    def get_queryset(self):
        """取得するオブジェクトの一覧を動的に変更する"""
        self.request.session['update_pre_page'] = 'product_list'#セッション保存
        Products = Product.objects.order_by('product_id')
        return Products

class ProductCreateView(LoginRequiredMixin,generic.CreateView):
    """品名登録画面"""
    model = Product
    template_name = 'PRO002_product_create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('asset_app:product_list')
 
    def form_valid(self,form):
        """バリデーションがうまくいったとき"""
        messages.success(self.request,'品名を登録しました')
        return super().form_valid(form)

    def form_invalid(self,form):
        """バリデーションがうまくいかなかったとき"""
        messages.error(self.request,"品名の登録を失敗しました")
        return super().form_invalid(form)

class ProductUpdateView(LoginRequiredMixin,generic.UpdateView):
    """品名編集画面"""
    model = Product
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

@require_POST
def ProductDeleteView(request, pk):
    """
    品名一覧画面の削除ボタンをクリックしたら品名を削除できる処理
    """
    # データが存在していることを確認する
    product = get_object_or_404(Product, product_id=pk)
    # productの削除
    Product.objects.filter(product_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'データを削除しました。')
    return redirect('asset_app:product_list')

class AssetListView(generic.ListView):
    """資産一覧画面"""
    model = Asset
    template_name = 'ASS001_asset_list.html'
    context_object_name = 'asset_list'
    paginate_by = 10
    #ProductとAssetの結合
    queryset = Asset.objects.select_related('product_ass_id')#prefetch_related('asset_ash_id')      
    
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
            PDT.PRODUCT_ID 
            , PDT.PRODUCT_NAME
            , COUNT(TEMP.STATUS < 3 OR NULL) AS AVAILABLE_CNT
            , COUNT(TEMP.STATUS < 5 OR NULL ) AS TOTAL_CNT
        FROM(
            SELECT
                AST.PRODUCT_ASS_ID_ID
                , ASH.ASSET_ASH_ID_ID
                , ASH.STATUS
                , ASH.UPDATE_DATE
            FROM
                ASSET_HISTORY ASH
                INNER JOIN ASSET AST
                ON ASH.ASSET_ASH_ID_ID = AST.ASSET_ID
            WHERE
                ASH.UPDATE_DATE = (
                    SELECT
                        MAX(UPDATE_DATE)
                    FROM
                        ASSET_HISTORY AS AH
                    WHERE
                        ASH.ASSET_ASH_ID_ID = AH.ASSET_ASH_ID_ID
                )
            AND	 ASH.DELETE = 0
            AND	 AST.DELETE = 0
        ) TEMP
        INNER JOIN PRODUCT PDT
            ON TEMP.PRODUCT_ASS_ID_ID = PDT.PRODUCT_ID
            AND PDT.DELETE = 0
        INNER JOIN ASSET A
            ON TEMP.ASSET_ASH_ID_ID = A.ASSET_ID
            AND A.DELETE = 0
        GROUP BY
            PDT.PRODUCT_ID
        ORDER BY
            PDT.PRODUCT_ID DESC; '''
        # 資産の使用可能数、総数を取得するSQL文
        asset_list_sql ='''
        SELECT
            PDT.PRODUCT_ID 
            ,A.MODEL_NAME
            ,COUNT(MD.STATUS < 3 OR NULL) AS AVAILABLE_CNT
            ,COUNT(MD.STATUS < 5 OR NULL) AS TOTAL_CNT
        FROM(
            SELECT
                AST.PRODUCT_ASS_ID_ID
                ,AST.MODEL_NAME
                , ASH.ASSET_ASH_ID_ID
                , ASH.STATUS
                , ASH.UPDATE_DATE
            FROM
                ASSET_HISTORY ASH
                INNER JOIN ASSET AST
                ON ASH.ASSET_ASH_ID_ID = AST.ASSET_ID
            WHERE
                ASH.UPDATE_DATE = (
                    SELECT
                        MAX(UPDATE_DATE)
                    FROM
                        ASSET_HISTORY AS AH
                    WHERE
                        ASH.ASSET_ASH_ID_ID = AH.ASSET_ASH_ID_ID
                )
            AND  ASH.DELETE = 0
            AND  AST.DELETE = 0
        ) MD
        INNER JOIN PRODUCT PDT
            ON MD.PRODUCT_ASS_ID_ID = PDT.PRODUCT_ID
            AND  PDT.DELETE = 0
        INNER JOIN ASSET A
            ON MD.ASSET_ASH_ID_ID = A.ASSET_ID
            AND MD.MODEL_NAME = A.MODEL_NAME
            AND A.DELETE = 0
        GROUP BY
            PDT.PRODUCT_ID,A.MODEL_NAME
        ORDER BY
            PDT.PRODUCT_ID DESC,A.MODEL_NAME DESC;'''
        product_list = AssetListView.get_count_product(product_list_sql)
        asset_list = AssetListView.get_count_asset(asset_list_sql)
        # 継承先のListViewのget_context_dataメソッドを実行し、それをcontext変数に代入しています。
        context = super(AssetListView, self).get_context_data(**kwargs)
        context.update({
            'product_list': Product.objects.all(),
            'asset_history_list' : Asset_History.objects.all(),
            'product_list' : product_list,
            'asset_list' : asset_list,
        })
        
        return context
        
    #     Assets = Asset.objects.order_by('asset_id')
    #     #Assets = Asset.objects.select_related('Product').prefetch_related('Asset_History')
    #     #Assets = Asset.objects.select_related('product_ass_id').all()
    #     return Assets

class AssetCreateView(LoginRequiredMixin,generic.CreateView):
    """資産登録画面"""
    model = Asset
    template_name = 'ASS002_asset_create.html'
    form_class = AssetCreateForm
    success_url = reverse_lazy('asset_app:asset_list')      
              
    def form_valid(self, form):
        """ 
        フォームを保存し、success_url を使用して 
        HttpResponseRedirect オブジェクトを返します
        """
        self.create_asset_object(self.request, form)
        return HttpResponseRedirect(self.get_success_url())
    
    def create_asset_object(self, request, form):
        """ オブジェクトを作成する機能 """        

        # DBから読み込み       
        product_abbreviation = Product.objects.get(product_name=form.cleaned_data['product_ass_id']).product_abbreviation

        #複数の入力フィールド値 取得
        serial_number_list = request.POST.getlist("serial_number")
        
        #DBから読んで同じ文字列の数をcountする
        count_serial_number = Asset.objects.filter(asset_id__icontains = "ALIBER-"+product_abbreviation+"-"+str(form.cleaned_data['purchase_date'])).count()
        
        #DBにcount_serial_numberが0ではない場合は+１、
        #0の場合は m=1
        if count_serial_number != 0:                
            m = count_serial_number+1
        else:
            m = 1

        #複数データ挿入   
        for serial_number in serial_number_list:
            self.object = Asset.objects.create(
                asset_id = "ALIBER-"+product_abbreviation+"-"+str(form.cleaned_data['purchase_date'])+"-"+str(m),
                model_name = form.cleaned_data['model_name'],
                storing_date = timezone.now(),
                purchase_date = form.cleaned_data['purchase_date'],
                serial_number = serial_number,
                delete = 0,
                create_date = timezone.now(),
                create_id = self.request.user.id,
                update_date = timezone.now(),
                update_id = self.request.user.id,
                product_ass_id_id = Product.objects.get(product_name__exact = form.cleaned_data['product_ass_id']).product_id,
                #num = m,
            )
            m = m + 1

            #データ挿入(asset_history)  実装待ち

    def form_invalid(self,form):
        messages.error(self.request,"品名の登録を失敗しました")
        return super().form_invalid(form)

# def get_absolute_url(self):
#     return reverse("asset:create_done", kwargs={
#         'product_ass_id': self.product_ass_id,
#         'model_name': self.model_name,
#         'storing_date': self.storing_date,
#         'asset_id': self.asset_id,
#         })

# def create_done(request,**kwargs):
#     contents = {}
#     for key,value in kwargs.items():
#         contents[key] = value
#     return render(request,'asset_create_done.html',{
#         'contents':contents,
#     })


class AssetView(LoginRequiredMixin,generic.DetailView):
    """資産詳細画面"""
    model = Asset
    template_name = "ASS004_asset.html"
    
    def get_context_data(self, **kwargs):
        self.request.session['update_pre_page'] = "asset"#セッション保存
        context = super().get_context_data(**kwargs)
        return context

def form_save(request, form, messages_success):
    Product = form.save(commit=False)
    Product.user = request.user
    Product.save()
    messages.success(request, messages_success)
    return form
