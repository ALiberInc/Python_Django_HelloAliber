from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from django.forms.forms import Form
from .models import EProfile, EDepartment
from accounts.models import CustomUser
import logging
import re
from django.forms.fields import DateField, IntegerField

# 210217 @ning about errormessage
from django.core.exceptions import ValidationError
def validate_lengh(value):
    if len(value) >20 :
        raise ValidationError(
            "漢字で正しく入力してください。",
            params={'value': value},
        )

logger = logging.getLogger(__name__)

class ProfileEditForm(ModelForm):
    class Meta:
        model = EProfile
        exclude = ("user", "department_pro_id", "created_at", "updated_at","delete","create_id","update_id","gender", "birth")
    # email = forms.EmailField(initial='',label='メールアドレス', required=True,)
    email = forms.CharField(initial='',label='メールアドレス', required=True,)
    gender_CHOICES=[('1','男性'),('0','女性'),]
    gender = forms.CharField(
        label='性別', 
        widget=forms.RadioSelect(choices=gender_CHOICES))
    birth = forms.CharField(label="生年月日", required=True)
    is_active = forms.CharField(
        label='アクティブ', 
        widget=forms.RadioSelect(choices=[('True','アクティブ'),('False','非アクティブ'),]))
    department_pro = forms.ModelChoiceField(EDepartment.objects, label='部門', initial=0)   
    field_order = ["user_id","last_name_k","first_name_k","last_name","first_name","gender","birth","email","nationality","phone","postal_code","address1","address2","residence_card","health_insurance","department_pro","emergency_contact_1_name","emergency_contact_1_relationship","emergency_contact_1_phone","emergency_contact_2_name","emergency_contact_2_relationship","emergency_contact_2_phone","emergency_contact_3_name","emergency_contact_3_relationship","emergency_contact_3_phone,is_active"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_id'].widget = forms.HiddenInput()
        self.fields['last_name_k'].required = True
        self.fields['last_name_k'].widget.attrs['maxlength'] = '20'
        self.fields['first_name_k'].required = True
        self.fields['first_name_k'].widget.attrs['maxlength'] = '20'
        self.fields['last_name'].widget.attrs['maxlength'] = '15'
        self.fields['first_name'].widget.attrs['maxlength'] = '15'
        self.fields['gender'].widget.attrs["class"] = "gender_class"
        self.fields['birth'].widget.attrs['maxlength'] = '8'
        self.fields['birth'].widget.attrs['placeholder'] = 'yyyymmdd'
        self.fields['email'].widget.attrs['maxlength'] = '30'
        self.fields['nationality'].required = True
        self.fields['nationality'].widget.attrs['maxlength'] = '20'
        self.fields['phone'].required = True
        self.fields['phone'].widget.attrs['maxlength'] = '15'
        self.fields['postal_code'].required = True
        self.fields['postal_code'].widget.attrs['maxlength'] = '10'
        self.fields['address1'].required = True
        self.fields['address1'].widget.attrs['placeholder'] = '都道府県名、または市区町村名を入力してください'
        self.fields['address1'].widget.attrs['maxlength'] = '50'
        self.fields['address2'].required = True
        self.fields['address2'].widget.attrs['placeholder'] = '町域名を入力してください'
        self.fields['address2'].widget.attrs['maxlength'] = '50'
        self.fields['residence_card'].widget.attrs['maxlength'] = '15'
        self.fields['health_insurance'].required = True
        self.fields['health_insurance'].widget.attrs['maxlength'] = '10'
        self.fields['department_pro'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_name'].required = True
        self.fields['emergency_contact_1_relationship'].required = True
        self.fields['emergency_contact_1_phone'].required = True
        self.fields['emergency_contact_1_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_1_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_2_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_2_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_2_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_3_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_3_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_3_phone'].widget.attrs['maxlength'] = '15'
        self.fields['is_active'].widget.attrs["class"] = "gender_class"
	    
        for field in self.fields.values():
            if field.required:
                field.error_messages = {'required': '「'+field.label+'」を入力してください。'}
    
    def clean_email(self):      
        email = self.cleaned_data.get('email')
        user_id = self.data.get('user_id')
        logger.debug("id={}".format(user_id))
        
        if not re.match(r"^[a-zA-Z0-9_+-]+(.[a-zA-Z0-9_+-]+)*@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$", email):
            raise forms.ValidationError("「メールアドレス」を正しく入力してください。")
        if email and CustomUser.objects.filter(email=email).exclude(id=user_id).count():
            raise forms.ValidationError("メールアドレスが既に存在しました。")
        if len(email) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        return self.cleaned_data["email"]

    def clean_last_name_k(self):
        last_name_k = self.data.get('last_name_k')
        if len(last_name_k) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        if not re.match(r"[ア-ン゛゜ァ-ォャ-ョー「」、]", last_name_k):
            raise forms.ValidationError("「姓（カタカナ）」はカタカナだけを入力してください。")
        return self.cleaned_data["last_name_k"]
    
    def clean_first_name_k(self):
        first_name_k = self.data.get('first_name_k')
        if len(first_name_k) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        if not re.match(r"[ア-ン゛゜ァ-ォャ-ョー「」、]", first_name_k):
            raise forms.ValidationError("「名（カタカナ）」はカタカナだけを入力してください。")
        return self.cleaned_data["first_name_k"]

    def clean_last_name(self):
        last_name = self.data.get('last_name')
        if len(last_name) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["last_name"]

    def clean_first_name(self):
        first_name = self.data.get('first_name')
        if len(first_name) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        return self.cleaned_data["first_name"]

    def clean_birth(self):
        birth = self.data.get('birth')
        if not re.match(r"[0-9]", birth):
            raise forms.ValidationError("「生年月日」は数字だけを入力してください")
        if len(birth) != 8:
            raise forms.ValidationError("8桁を入力してください。")
        return self.cleaned_data["birth"]

    def clean_nationality(self):
        nationality = self.data.get('nationality')
        if len(nationality) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["nationality"]

    def clean_phone(self):
        phone = self.data.get('phone')
        if len(phone) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        if not re.match(r"[0-9]", phone):
            raise forms.ValidationError("「携帯電話」は数字だけを入力してください。")
        return self.cleaned_data["phone"]

    def clean_postal_code(self):
        postal_code = self.data.get('postal_code')
        if len(postal_code) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        if not re.match(r"[0-9\-]", postal_code):
            raise forms.ValidationError("「郵便番号」は数字だけを入力してください。")
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
        if residence_card !="" and not re.match(r"[0-9a-zA-Z]", residence_card):
            raise forms.ValidationError("「在留カード番号」は英数字だけを入力してください。")
        return self.cleaned_data["residence_card"]

    def clean_health_insurance(self):
        health_insurance = self.data.get('health_insurance')
        if len(health_insurance) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        if not re.match(r"[0-9]", health_insurance):
            raise forms.ValidationError("「健康保険番号」は数字だけを入力してください。")
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
        if not re.match(r"[0-9]", emergency_contact_1_phone):
            raise forms.ValidationError("「電話番号」は数字だけを入力してください。")
        return self.cleaned_data["emergency_contact_1_phone"]

    def clean_emergency_contact_2_name(self):
        emergency_contact_2_name = self.data.get('emergency_contact_2_name')
        if len(emergency_contact_2_name) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_2_name"]

    def clean_emergency_contact_2_relationship(self):
        emergency_contact_2_relationship = self.data.get('emergency_contact_2_relationship')
        if len(emergency_contact_2_relationship) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_2_relationship"]

    def clean_emergency_contact_2_phone(self):
        emergency_contact_2_phone = self.data.get('emergency_contact_2_phone')
        if len(emergency_contact_2_phone) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        if emergency_contact_2_phone != "" and not re.match(r"[0-9]", emergency_contact_2_phone):
            raise forms.ValidationError("「電話番号」は数字だけを入力してください。")
        return self.cleaned_data["emergency_contact_2_phone"]

    def clean_emergency_contact_3_name(self):
        emergency_contact_3_name = self.data.get('emergency_contact_3_name')
        if len(emergency_contact_3_name) > 20:
            raise forms.ValidationError("20桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_3_name"]

    def clean_emergency_contact_3_relationship(self):
        emergency_contact_3_relationship = self.data.get('emergency_contact_3_relationship')
        if len(emergency_contact_3_relationship) > 10:
            raise forms.ValidationError("10桁以内を入力してください。")
        return self.cleaned_data["emergency_contact_3_relationship"]

    def clean_emergency_contact_3_phone(self):
        emergency_contact_3_phone = self.data.get('emergency_contact_3_phone')
        if len(emergency_contact_3_phone) > 15:
            raise forms.ValidationError("15桁以内を入力してください。")
        if emergency_contact_3_phone != "" and not re.match(r"[0-9]", emergency_contact_3_phone):
            raise forms.ValidationError("「電話番号」は数字だけを入力してください。")
        return self.cleaned_data["emergency_contact_3_phone"]

class DepartmentEditForm(ModelForm):
    class Meta:
        model = EDepartment
        exclude = ("delete", "create_date", "create_id","update_date","update_id")
    establish_date = forms.DateField(label = '設立日',widget=forms.DateInput(attrs={'type': 'date'}))
    dep_id = IntegerField(initial=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dep_id'].widget = forms.HiddenInput()
        self.fields['dep_id'].required = False
        self.fields['department'].widget.attrs['maxlength'] = '30'
        self.fields['department'].required = True
        self.fields['department'].widget.attrs['placeholder'] = '例:営業部'
        self.fields['department'].error_messages = {
            'required': '部門名を入力してください。',
            'maxlength':'30桁以内を入力してください。'}
        self.fields['establish_date'].required = True
        self.fields['establish_date'].error_messages = {
            'required': '設立日を入力してください。'}

        for field in self.fields.values():
            if field.required:
                field.error_messages = {'required' : '「'+str(field.label)+'」を入力してください。'}
        
    def clean_department(self):
        department = self.data.get('department')
        id = self.data.get('dep_id')
        if len(department) > 30:
            raise forms.ValidationError("30桁以内を入力してください。")
        if department and EDepartment.objects.filter(department = department).filter(delete=0).exclude(dep_id=id).count():
            raise forms.ValidationError("部門が既に存在しました。") 
        return self.cleaned_data["department"]