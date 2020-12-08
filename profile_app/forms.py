from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from .models import Profile, Department
from accounts.models import CustomUser
from django.forms import MultiWidget
import logging
import json
import sys
import requests

logger = logging.getLogger(__name__)

class ProfileCreateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("last_name", "first_name", "department_pro")

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("user", "created_at", "updated_at","user_id","delete","create_id","update_id","gender")
    email = forms.EmailField(initial='',label='メールアドレス', required=True,)
    gender_CHOICES=[('1','男性'),('0','女性'),]
    gender = forms.CharField(
        label='性別', 
        widget=forms.RadioSelect(choices=gender_CHOICES))
    is_active = forms.CharField(
        label='アクティブ', 
        widget=forms.RadioSelect(choices=[('True','アクティブ'),('False','非アクティブ'),]))

    field_order = ["last_name_k","first_name_k","last_name","first_name","gender","birth","email","nationality","phone","postal_code","address1","address2","residence_card","health_insurance","department_pro","emergency_contact_1_name","emergency_contact_1_relationship","emergency_contact_1_phone","emergency_contact_2_name","emergency_contact_2_relationship","emergency_contact_2_phone","emergency_contact_3_name","emergency_contact_3_relationship","emergency_contact_3_phone,is_active"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields.values():
        #     field.widget.attrs["class"] = "form-control"
        self.fields['id'].widget = forms.HiddenInput()
        self.fields['last_name_k'].widget.attrs['pattern'] = '^[ア-ン゛゜ァ-ォャ-ョー「」、]+$'
        self.fields['last_name_k'].required = True
        self.fields['last_name_k'].error_messages = {'required': self.fields['last_name_k'].label+'を入力してください。'}
        self.fields['first_name_k'].widget.attrs['pattern'] = '^[ア-ン゛゜ァ-ォャ-ョー「」、]+$'
        self.fields['first_name_k'].required = True
        self.fields['first_name_k'].error_messages = {'required': self.fields['first_name_k'].label+'を入力してください。'}
        self.fields['last_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['last_name'].error_messages = {'required': self.fields['last_name'].label+'を入力してください。'}
        self.fields['first_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['first_name'].error_messages = {'required': self.fields['first_name'].label+'を入力してください。'}
        self.fields['gender'].widget.attrs["class"] = "gender_class"
        self.fields['email'].widget.attrs['pattern'] = '^([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9\._-]+)+$'
        self.fields['email'].error_messages = {'required': self.fields['email'].label+'を入力してください。'}
        self.fields['nationality'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['nationality'].required = True
        self.fields['nationality'].error_messages = {'required': self.fields['nationality'].label+'を入力してください。'}
        self.fields['phone'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['phone'].required = True
        self.fields['phone'].error_messages = {'required': self.fields['phone'].label+'を入力してください。'}
        self.fields['postal_code'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['postal_code'].required = True
        self.fields['postal_code'].error_messages = {'required': self.fields['postal_code'].label+'を入力してください。'}
        self.fields['address1'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['address1'].required = True
        self.fields['address1'].error_messages = {'required': self.fields['address1'].label+'を入力してください。'}
        self.fields['address2'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['address2'].required = True
        self.fields['address2'].error_messages = {'required': self.fields['address2'].label+'を入力してください。'}
        self.fields['residence_card'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'
        # self.fields['residence_card'].required = True
        self.fields['residence_card'].error_messages = {'required': self.fields['residence_card'].label+'を入力してください。'}
        self.fields['health_insurance'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'
        self.fields['health_insurance'].required = True
        self.fields['health_insurance'].error_messages = {'required': self.fields['health_insurance'].label+'を入力してください。'}
        self.fields['department_pro'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_1_name'].required = True
        self.fields['emergency_contact_1_name'].error_messages = {'required': self.fields['emergency_contact_1_name'].label+'を入力してください。'}
        self.fields['emergency_contact_1_relationship'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_1_relationship'].required = True
        self.fields['emergency_contact_1_relationship'].error_messages = {'required': self.fields['emergency_contact_1_relationship'].label+'を入力してください。'}
        self.fields['emergency_contact_1_phone'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['emergency_contact_1_phone'].required = True
        self.fields['emergency_contact_1_phone'].error_messages = {'required': self.fields['emergency_contact_1_phone'].label+'を入力してください。'}
        self.fields['emergency_contact_2_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_2_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_2_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_2_relationship'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_2_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_2_phone'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['emergency_contact_3_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_3_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_3_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_3_relationship'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_3_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_3_phone'].widget.attrs['pattern'] = '^[0-9]+$'
    
    def clean_email(self):      
        email = self.cleaned_data.get('email')
        id = self.data.get('id')
        logger.debug("id={}".format(id))
        
        if email and CustomUser.objects.filter(email=email).exclude(id=id).count():
            raise forms.ValidationError("メールアドレスが既に存在しました。")
        elif len(email) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        return self.cleaned_data["email"]

    def clean_last_name_k(self):
        last_name_k = self.data.get('last_name_k')
        if len(last_name_k) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["last_name_k"]
    
    def clean_first_name_k(self):
        first_name_k = self.data.get('first_name_k')
        if len(first_name_k) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["first_name_k"]

    def clean_last_name(self):
        last_name = self.data.get('last_name')
        if len(last_name) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["last_name"]

    def clean_first_name(self):
        first_name = self.data.get('first_name')
        if len(first_name) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["first_name"]

    def clean_nationality(self):
        nationality = self.data.get('nationality')
        if len(nationality) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["nationality"]

    def clean_phone(self):
        phone = self.data.get('phone')
        if len(phone) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["phone"]

    def clean_postal_code(self):
        postal_code = self.data.get('postal_code')
        if len(postal_code) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["postal_code"]

    def clean_address1(self):
        address1 = self.data.get('address1')
        if len(address1) > 50:
            raise forms.ValidationError("50桁以内を入力してください。")
        return self.cleaned_data["address1"]

    def clean_address2(self):
        address2 = self.data.get('address2')
        if len(address2) > 50:
            raise forms.ValidationError("50桁以内を入力してください。")
        return self.cleaned_data["address2"]

    def clean_residence_card(self):
        residence_card = self.data.get('residence_card')
        if len(residence_card) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["residence_card"]

    def clean_health_insurance(self):
        health_insurance = self.data.get('health_insurance')
        if len(health_insurance) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["health_insurance"]

    def clean_emergency_contact_1_name(self):
        emergency_contact_1_name = self.data.get('emergency_contact_1_name')
        if len(emergency_contact_1_name) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_1_name"]

    def clean_emergency_contact_1_relationship(self):
        emergency_contact_1_relationship = self.data.get('emergency_contact_1_relationship')
        if len(emergency_contact_1_relationship) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_1_relationship"]

    def clean_emergency_contact_1_phone(self):
        emergency_contact_1_phone = self.data.get('emergency_contact_1_phone')
        if len(emergency_contact_1_phone) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_1_phone"]
        