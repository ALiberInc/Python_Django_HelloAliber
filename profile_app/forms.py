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
        exclude = ("user", "created_at", "updated_at","id","user_id","delete","create_id","update_id","gender")
    email = forms.EmailField(initial='',label='メールアドレス', required=True,)
    gender_CHOICES=[('1','男性'),('0','女性'),]
    gender = forms.CharField(label='性別', widget=forms.RadioSelect(choices=gender_CHOICES))
   
    field_order = ["last_name_k","first_name_k","last_name","first_name","gender","birth","email","nationality","phone","postal_code","address1","address2","residence_card","health_insurance","department_pro","emergency_contact_1_name","emergency_contact_1_relationship","emergency_contact_1_phone","emergency_contact_2_name","emergency_contact_2_relationship","emergency_contact_2_phone","emergency_contact_3_name","emergency_contact_3_relationship","emergency_contact_3_phone"]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields.values():
        #     field.widget.attrs["class"] = "form-control"
      
        self.fields['last_name_k'].widget.attrs['maxlength'] = '10'
        self.fields['last_name_k'].widget.attrs['pattern'] = '^[ア-ン゛゜ァ-ォャ-ョー「」、]+$'
        self.fields['last_name_k'].widget.attrs['required'] = 'Ture'
        self.fields['first_name_k'].widget.attrs['maxlength'] = '10'
        self.fields['first_name_k'].widget.attrs['pattern'] = '^[ア-ン゛゜ァ-ォャ-ョー「」、]+$'
        self.fields['first_name_k'].widget.attrs['required'] = 'Ture'
        self.fields['last_name'].widget.attrs['maxlength'] = '10'
        self.fields['last_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['first_name'].widget.attrs['maxlength'] = '10'
        self.fields['first_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['email'].widget.attrs['maxlength'] = '30'
        self.fields['email'].widget.attrs['pattern'] = '^([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9\._-]+)+$'
        self.fields['nationality'].widget.attrs['maxlength'] = '20'
        self.fields['nationality'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['nationality'].widget.attrs['required'] = 'Ture'
        self.fields['phone'].widget.attrs['maxlength'] = '15'
        self.fields['phone'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['phone'].widget.attrs['required'] = 'Ture'
        self.fields['postal_code'].widget.attrs['maxlength'] = '10'
        self.fields['postal_code'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['address1'].widget.attrs['maxlength'] = '50'
        self.fields['address1'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['address1'].widget.attrs['required'] = 'Ture'
        self.fields['address2'].widget.attrs['maxlength'] = '50'
        self.fields['address2'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['address2'].widget.attrs['required'] = 'Ture'
        self.fields['residence_card'].widget.attrs['maxlength'] = '15'
        self.fields['residence_card'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'
        self.fields['residence_card'].widget.attrs['required'] = 'Ture'
        self.fields['health_insurance'].widget.attrs['maxlength'] = '10'
        self.fields['health_insurance'].widget.attrs['pattern'] = '^[a-zA-Z0-9]+$'
        self.fields['health_insurance'].widget.attrs['required'] = 'Ture'
        self.fields['department_pro'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_1_name'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_1_name'].widget.attrs['required'] = 'Ture'
        self.fields['emergency_contact_1_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_relationship'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['emergency_contact_1_relationship'].widget.attrs['required'] = 'Ture'
        self.fields['emergency_contact_1_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_1_phone'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['emergency_contact_1_phone'].widget.attrs['required'] = 'Ture'
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

    # def clean_email(self):
    #     cleaned_data = super().clean()
    #     v_email = cleaned_data.get('email')
    #     try 
    #     user = Profile.objects.filter(email=v_email).count():
    #         raise forms.ValidationError('メールアドレスが既に存在しました。')
    #     except 
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        # id_value = Profile.objects.get(user_id__exact=self.kwargs['pk']).id_id
        # email_old = CustomUser.objects.get(id__exact=id_value).email
        # if email_old == email:
        #     return email_old
        # else:
        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return email
        raise forms.ValidationError("メールアドレスが既に存在しました。")