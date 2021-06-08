from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.forms.fields import DateField, IntegerField
from django.forms.forms import Form
from django.forms.widgets import DateInput
from .models import Product,Asset,Asset_History
from accounts.models import CustomUser
from django.forms import MultiWidget
import six


class ProductEditForm(forms.ModelForm):
    
    class Meta:    
        model = Product
        #exclude = ("created_date", "updated_date","delete","create_id","update_id",)
        fields = ("product_id", "product_name", "product_abbreviation" )
    #0517寧 自身のデータと重複するので、更新できないについて修正
    #product_name_old = forms.CharField(label="品名_old", initial='',required=False)
    #product_abbreviation_old = forms.CharField(label="略称_old", initial='',required=False)
    product_id = IntegerField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_id'].widget = forms.HiddenInput()
        #self.fields['product_name_old'].widget = forms.HiddenInput()
        #self.fields['product_abbreviation_old'].widget = forms.HiddenInput()
        self.fields['product_id'].required = False
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
                field.error_messages = {'required' : '「'+str(field.label)+'」を入力してください。'}

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        #product_name_old = self.data.get('product_name_old')
        id = self.data.get('product_id')
        if len(product_name) > 50:
            raise forms.ValidationError("50桁以内を入力してください。") 
        
        # if product_name != product_name_old and Product.objects.filter(product_name=product_name).count():
        #     raise forms.ValidationError("品名が既に存在しました。")
        # return self.cleaned_data["product_name"]
        if product_name and Product.objects.filter(product_name=product_name).exclude(product_id=id).count():
            raise forms.ValidationError("品名が既に存在しました。")
        return self.cleaned_data["product_name"]

    def clean_product_abbreviation(self):
        product_abbreviation = self.cleaned_data.get('product_abbreviation')
        #product_abbreviation_old = self.data.get('product_abbreviation_old')
        id = self.data.get('product_id')
        if len(product_abbreviation) > 50:
            raise forms.ValidationError("50桁以内を入力してください。")
        # if product_abbreviation != product_abbreviation_old and Product.objects.filter(product_abbreviation=product_abbreviation).count():
        #     raise forms.ValidationError("略称が既に存在しました。")
        # return self.cleaned_data["product_abbreviation"]
        if product_abbreviation and Product.objects.filter(product_abbreviation=product_abbreviation).exclude(product_id=id).count():
            raise forms.ValidationError("略称が既に存在しました。")
        return self.cleaned_data["product_abbreviation"]
    
class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ("product_ass_id","model_name","purchase_date","serial_number",)
    purchase_date = forms.DateField(label = '購入日',widget=forms.DateInput(attrs={'type': 'date'}))
    # field_order = ["product_ass_id","model_name","purchase_date","serial_number"]
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['asset_id'] = forms.CharField(label='資産番号', initial="", )
        self.fields['product_ass_id'].widget.attrs['maxlength'] = '100'
        self.fields['product_ass_id'].required = True
        #品名inita=0追加
        #self.fields['product_ass_id'].
        self.fields['product_ass_id'].error_messages = {
            'required': '品名を選択してください。',
            'maxlength':'100桁以内を入力してください。'}
        self.fields['model_name'].widget.attrs['maxlength'] = '100'
        self.fields['model_name'].required = True
        self.fields['model_name'].widget.attrs['placeholder'] = 'HP'
        self.fields['model_name'].error_messages = {
            'required': 'モデル名を入力してください。',
            'maxlength':'100桁以内を入力してください。'}
        self.fields['purchase_date'].required = True
        self.fields['purchase_date'].error_messages = {
            'required': '購入日を選択してください。',}
        self.fields['serial_number'].widget.attrs['maxlength'] = '100'
        self.fields['serial_number'].required = True
        self.fields['serial_number'].error_messages = {
            'required': '識別番号を入力してください。',
            'maxlength':'100桁以内を入力してください。'}

        for field in self.fields.values():
            if field.required:
                field.error_messages = {'required' : '「'+str(field.label)+'」を入力してください。'}

    def clean_model_name(self):
        model_name = self.cleaned_data.get('model_name')
        id = self.data.get('asset_id')
        if len(model_name) > 50:
            raise forms.ValidationError("50桁以内を入力してください。") 
        return self.cleaned_data["model_name"]

    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('purchase_date')
        id = self.data.get('asset_id')
        return self.cleaned_data["purchase_date"]

    def clean_serial_number(self):
        serial_number = self.cleaned_data.get('serial_number')
        id = self.data.get('asset_id')
        if len(serial_number) > 100:
            raise forms.ValidationError("50桁以内を入力してください。") 
        return self.cleaned_data["serial_number"]
        