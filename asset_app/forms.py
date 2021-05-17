from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.forms.forms import Form
from .models import Product,Asset,Asset_History
from accounts.models import CustomUser
from django.forms import MultiWidget
import six
#from django.forms import ProductCreateForm

class ProductEditForm(forms.ModelForm):
    
    class Meta:    
        model = Product
        #exclude = ("created_date", "updated_date","delete","create_id","update_id",)
        fields = ("product_id", "product_name", "product_abbreviation" )
    #product_name = forms.CharField(label="品名", required=True)
    #product_abbreviation = forms.CharField(label="略称", required=True)

    def __init__(self, *args, **kwargs):
        #id = kwargs.pop('product_id')
        super().__init__(*args, **kwargs)
        #self.fields['id'] = forms.IntegerField(disabled = True,widget = forms.HiddenInput())
        self.fields['product_name'].widget.attrs['maxlength'] = '50'
        self.fields['product_name'].required = True
        self.fields['product_name'].widget.attrs['placeholder'] = '例:デスクトップ'
        self.fields['product_name'].error_messages = {
            'required': '品名を入力してください。',
            'maxlength':'50桁以内を入力してください。'}
        self.fields['product_abbreviation'].widget.attrs['maxlength'] = '50'
        self.fields['product_abbreviation'].required = True
        self.fields['product_abbreviation'].widget.attrs['placeholder'] = '例:desktop'
        self.fields['product_abbreviation'].error_messages = {
            'required': '略称を入力してください。',
            'maxlength':'50桁以内を入力してください。'}
        
        for field in self.fields.values():
            if field.required:
                field.error_messages = {'required' : '「'+field.label+'」を入力してください。'}
        # for field in self.fields.values():
        #     if 'required' in field.error_messages:
        #         field.error_messages['required'] = '「'+field.label+'」を入力してください。'

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        #for k,v in six.iteritems(self.data):
            #print(k,v)
        id = self.data.get('product_id')
        if len(product_name) > 50:
            raise forms.ValidationError("50桁以内を入力してください。") 
        #print(self.param.get("product_id"))      
        #print(Product.objects.filter(product_name=product_name).exclude(product_id=id))
        #print("adfa"+str(id))
        #print(attr(self))
        #print(attr(self.data))       
        if product_name and Product.objects.filter(product_name=product_name).exclude(product_id=id).count():
            raise forms.ValidationError("品名が既に存在しました。")
        return self.cleaned_data["product_name"]

    def clean_product_abbreviation(self):
        product_abbreviation = self.cleaned_data.get('product_abbreviation')
        id = self.data.get('product_id')
        if len(product_abbreviation) > 50:
            raise forms.ValidationError("50桁以内を入力してください。")
        if product_abbreviation and Product.objects.filter(product_abbreviation=product_abbreviation).exclude(product_id=id).count():
            raise forms.ValidationError("略称が既に存在しました。")
        return self.cleaned_data["product_abbreviation"]        
    
class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ("product_ass_id","model_name","purchase_date","serial_number",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_ass_id'].widget.attrs['maxlength'] = '100'
        self.fields['product_ass_id'].required = True
        self.fields['product_ass_id'].widget.attrs['placeholder'] = 'デスクトップ'
        self.fields['product_ass_id'].error_messages = {
            'required': '品名を選択してください。',
            'maxlength':'100桁以内を入力してください。'}
        self.fields['model_name'].widget.attrs['maxlength'] = '100'
        self.fields['model_name'].required = True
        self.fields['model_name'].widget.attrs['placeholder'] = 'HP'
        self.fields['model_name'].error_messages = {
            'required': 'モデル名を入力してください。',
            'maxlength':'100桁以内を入力してください。'}
        self.fields['purchase_date'].widget.attrs['maxlength'] = '100'
        self.fields['purchase_date'].required = True
        self.fields['purchase_date'].widget.attrs['placeholder'] = 'デスクトップ'
        self.fields['purchase_date'].error_messages = {
            'required': '購入日を入力してください。',
            'maxlength':'100桁以内を入力してください。'}
        self.fields['serial_number'].widget.attrs['maxlength'] = '100'
        self.fields['serial_number'].required = True
        self.fields['serial_number'].widget.attrs['placeholder'] = 'PDD63HI'
        self.fields['serial_number'].error_messages = {
            'required': '識別番号を入力してください。',
            'maxlength':'100桁以内を入力してください。'}

        for field in self.fields.values():
            if field.required:
                field.error_messages = {'required' : '「'+field.label+'」を入力してください。'}