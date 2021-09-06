from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.forms import fields
from django.forms.fields import DateField, IntegerField
from django.forms.forms import Form
from django.forms.widgets import DateInput

from profile_app.models import EDepartment, EProfile
from .models import Product,Asset,Asset_History
from accounts.models import CustomUser
from django.forms import MultiWidget
import six
import re

from django.core.exceptions import ValidationError
def validate_lengh(value):
    if len(value) >50 :
        raise ValidationError(
            "漢字で正しく入力してください。",
            params={'value': value},
        )

class ProductEditForm(forms.ModelForm):
    
    class Meta:    
        model = Product
        #exclude = ("created_date", "updated_date","delete","create_id","update_id",)
        fields = ("product_id", "product_name", "product_abbreviation" )
    product_id = IntegerField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        product_name = self.data.get('product_name')
        id = self.data.get('product_id')
        if len(product_name) > 50:
            raise forms.ValidationError("50桁以内を入力してください。")        
        if product_name and Product.objects.filter(product_name=product_name).exclude(product_id=id).count():
            raise forms.ValidationError("品名が既に存在しました。")
        return self.cleaned_data["product_name"]

    def clean_product_abbreviation(self):
        product_abbreviation = self.data.get('product_abbreviation')
        product_abbreviation_old = self.data.get('product_abbreviation_old')
        id = self.data.get('product_id')
        if len(product_abbreviation) > 50:
            raise forms.ValidationError("50桁以内を入力してください。")
        if not re.match(r"[a-zA-Z0-9_+-]", product_abbreviation):
            raise forms.ValidationError("半角英数字及び「_」「-」を入力してください")
            raise forms.ValidationError("略称が既に存在しました。")
        return self.cleaned_data["product_abbreviation"]
    
class AssetCreateForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ("product_ass_id","model_name","purchase_date","serial_number",)
    purchase_date = forms.DateField(label = '購入日',widget=forms.DateInput(attrs={'type': 'date'}))
    # field_order = ["product_ass_id","model_name","purchase_date","serial_number"]
    asset_id = IntegerField(initial=0)   

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset_id'].widget = forms.HiddenInput()
        self.fields['asset_id'].required = False
        #self.fields['asset_id'] = forms.CharField(label='資産番号', initial="", )
        self.fields['product_ass_id'].widget.attrs['maxlength'] = '100'
        self.fields['product_ass_id'].required = True
        #品名inita=0追加
        #self.fields['product_ass_id'].
        self.fields['product_ass_id'].error_messages = {
            'required': '品名を選択してください。',
            'maxlength':'50桁以内を入力してください。'}
        self.fields['model_name'].widget.attrs['maxlength'] = '50'
        self.fields['model_name'].required = True
        #self.fields['model_name'].widget.attrs['placeholder'] = 'HP'
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
        model_name = self.data.get('model_name')
        if len(model_name) > 50:
            raise forms.ValidationError("50桁以内を入力してください。") 
        return self.cleaned_data["model_name"]

    # def clean_purchase_date(self):
    #     purchase_date = self.data.get('purchase_date')
    #     asset_id = self.data.get('asset_id')
    #     return self.cleaned_data["purchase_date"]

    def clean_serial_number(self):
        serial_number = self.data.get('serial_number')
        print("これは"+serial_number)
        asset_id = self.data.get('asset_id')
        if len(serial_number) > 100:
            raise forms.ValidationError("100桁以内を入力してください。")
        if serial_number and Asset.objects.filter(serial_number=serial_number).exclude(asset_id=asset_id).count():
            raise forms.ValidationError("識別番号が既に存在しました。")
        return self.cleaned_data["serial_number"]

    # def clean(self):
    #     super().clean()
    #     serial_number = self.cleaned_data['serial_number']
    #     serial_number = self.data.get('serial_number')
    #     if serial_number == serial_number:
    #         raise forms.ValidationError("同じ識別番号を入力しないようにしてください。")
    # def clean(self):
    #     all_clean_data = super(AssetCreateForm,self).clean()
    #     serial_number = all_clean_data['serial_number']
    #     print(serial_number)
    #     if serial_number == serial_number:
    #         self.add_error('serial_number','同じ識別番号を入力しないようにしてください。')
    #    return all_clean_data

class AssetHistoryCreateForm(forms.ModelForm):
    class Meta:
        model = EDepartment
        fields = '__all__'
        
    department = forms.ModelChoiceField(
        label = '部門',
        queryset = EDepartment.objects,
        required = False
    )

    profile = forms.ModelChoiceField(
        label = '利用者',
        queryset = EProfile.objects.none(),
        required = False 
    )

    field_order = ('department','profile')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)