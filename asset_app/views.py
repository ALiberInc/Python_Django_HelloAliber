from django.shortcuts import render
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

def index(request):
    return HttpResponse("Hello.")

class ProductListView(generic.ListView):
    """品名一覧画面"""
    model = Product
    template_name = 'PRO001_product_list.html'
    context_object_name = 'product_list'
    paginate_by = 10

    def get_queryset(self):
        self.request.session['update_pre_page'] = 'product_list'#セッション保存
        Products = Product.objects.order_by('product_id')
        return Products

class ProductCreateView(LoginRequiredMixin,generic.CreateView):
    """品名登録画面"""
    model = Product
    template_name = 'PRO002_product_create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('asset_app:product_list')
    
    # def post_form(request):
    #     if request.method == "POST" and request.POST["product_name"] and request.POST["product_abbreviation"]:
    #         Product = Product.objects.create(
    #             product_name=request.POST["product_name"],
    #             product_abbreviation=request.POST["product_abbreviation"]
    #         )
    #         Product.save()
    #         return HttpResponse("保存完了")
    #     else:
    #         return HttpResponse("必須項目がPOSTされていません")
    
    # def productcreate(request):
    #     if request.method == 'POST':
    #         form = ProductCreateForm(request.POST)
    #         if form.is_valid():
    #             data_pro = form.save(commit=False)
    #             data_pro.save()
    #     else:
    #         form = ProductCreateForm()
    #     return render(request,'asset_app/product_list.html',{'form': form})

    # def product_create(request):
    #     form = ProductCreateForm(request.post or None)
    #     if form.is_valid():
    #         models.Product.objects.create(**form.cleaned_data)
    #         return redirect('asset_app:product_list')

    #     p = {
    #         'form' : form,
    #         'product_qs' : models.Procuct.objects.all().order_by('product_id')
    #     }

    #     return render(request,'asset_app/asset_create.html',p)

    #def form_valid(self,form):
        # if request.method == 'POST':
        #     form = ProductCreateForm(request.POST)
        #     if request.POST['id']:
        #         try:
        #         Product = Product.objects.get(pk=request.POST['product_id'])
        #         form.instance = p
        #         except Product.DoesNotExist:
        #         pass
        #messages.success(self.request,'品名を登録しました')
        #return super().form_valid(form)

    def form_valid(self,form):
        messages.success(self.request,'品名を登録しました')
        return super().form_valid(form)

    def form_invalid(self,form):
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
        form_kwargs = super().get_form_kwargs(*args, **kwargs)

        #DBから読み込み
        product_name_value = Product.objects.get(product_id__exact=self.kwargs['pk']).product_name
        product_abbreviation_value = Product.objects.get(product_id__exact=self.kwargs['pk']).product_abbreviation
        #Form初期値を設定する
        form_kwargs['initial'] = {
            'product_name' : product_name_value,
            'product_abbreviation' : product_abbreviation_value,
        }
        return form_kwargs

    def form_valid(self,form):
        messages.success(self.request,"品名の登録しました")
        # form = form_save(self.request,form,'品名を登録しました')
        # # formのデータ取得
        # product_name_cleaned = self.request.POST['product_name']
        # product_abbreviation_cleaned = self.request.POST['product_abbreviation']
        # Product.objects.filter(product_id = product_id)
        # # DB登録
        # Product.objects.filter(product_id = product_id).update(
        #     product_name = product_name_cleaned,
        #     product_abbreviation = product_abbreviation_cleaned,
        # )
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,"品名の登録を失敗しました")
        return super().form_invalid(form)

@require_POST
def ProductDeleteView(request, pk):
    product = get_object_or_404(Product, product_id=pk)
    Product.objects.filter(product_id=pk).delete()
    messages.add_message(request, messages.SUCCESS, 'データを削除しました。')
    return redirect('asset_app:product_list')

class AssetListView(generic.ListView):
    """資産一覧画面"""
    model = Asset
    template_name = 'ASS001_asset_list.html'
    context_object_name = 'asset_list'
    paginate_by = 10

    def get_queryset(self):
        Assets = Asset.objects.order_by('asset_id')
        return Assets

class AssetCreateView(LoginRequiredMixin,generic.CreateView):
    """資産登録画面"""
    model = Asset
    template_name = 'ASS002_asset_create.html'
    form_class = AssetCreateForm
    success_url = reverse_lazy('asset_app:asset_create_done')

    def form_valid(self,form):
        messages.error(self.request,"品名の登録しました")
        return super().form_valid(form)

    def form_invalid(self,form):
        messages.error(self.request,"品名の登録を失敗しました")
        return super().form_invalid(form)

def form_save(request, form, messages_success):
    Product = form.save(commit=False)
    Product.user = request.user
    Product.save()
    messages.success(request, messages_success)
    return form
