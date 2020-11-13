from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from .models import Profile, Department
from accounts.models import CustomUser
from django.forms import MultiWidget
import logging

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
    gender_CHOICES=[
    ('1','男性'),
    ('0','女性'),
    ]
    gender = forms.CharField(label='性別', widget=forms.RadioSelect(choices=gender_CHOICES))
    field_order = ["last_name_k","first_name_k","last_name","first_name","gender","birth","email","nationality","phone","postal_code","address1","address2","residence_card","health_insurance","department_pro","emergency_contact_1_name","emergency_contact_1_relationship","emergency_contact_1_phone","emergency_contact_2_name","emergency_contact_2_relationship","emergency_contact_2_phone","emergency_contact_3_name","emergency_contact_3_relationship","emergency_contact_3_phone"]
        
    def __init__(self, *args, **kwargs):
        super(ProfileEditForm,self).__init__(*args, **kwargs)
        # for field in self.fields.values():
        #     field.widget.attrs["class"] = "form-control"
      
        self.fields['last_name_k'].widget.attrs['maxlength'] = '10'
        self.fields['last_name_k'].widget.attrs['pattern'] = '^[ア-ン゛゜ァ-ォャ-ョー「」、]+$'
        self.fields['first_name_k'].widget.attrs['maxlength'] = '10'
        self.fields['first_name_k'].widget.attrs['pattern'] = '^[ア-ン゛゜ァ-ォャ-ョー「」、]+$'
        self.fields['last_name'].widget.attrs['maxlength'] = '10'
        self.fields['last_name'].widget.attrs['pattern'] = '^[あ-ん゛゜ぁ-ぉゃ-ょー「」、]+'
        self.fields['first_name'].widget.attrs['maxlength'] = '10'
        self.fields['first_name'].widget.attrs['pattern'] = '^[あ-ん゛゜ぁ-ぉゃ-ょー「」、]+'
        self.fields['email'].widget.attrs['maxlength'] = '30'
        self.fields['email'].widget.attrs['pattern'] = '^([a-zA-Z0-9])+([a-zA-Z0-9\._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9\._-]+)+$'
        self.fields['nationality'].widget.attrs['maxlength'] = '20'
        self.fields['nationality'].widget.attrs['pattern'] = '^[ぁ-んァ-ヶー一-龠]+$'
        self.fields['phone'].widget.attrs['maxlength'] = '15'
        self.fields['phone'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['postal_code'].widget.attrs['maxlength'] = '10'
        self.fields['postal_code'].widget.attrs['pattern'] = '^[0-9]+$'
        self.fields['address1'].widget.attrs['maxlength'] = '50'
        # self.fields['address1'].widget.attrs['pattern'] = '50'
        self.fields['address2'].widget.attrs['maxlength'] = '50'
        # self.fields['address2'].widget.attrs['pattern'] = '50'
        self.fields['residence_card'].widget.attrs['maxlength'] = '15'
        self.fields['health_insurance'].widget.attrs['maxlength'] = '10'
        self.fields['department_pro'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_1_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_1_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_2_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_2_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_2_phone'].widget.attrs['maxlength'] = '15'
        self.fields['emergency_contact_3_name'].widget.attrs['maxlength'] = '20'
        self.fields['emergency_contact_3_relationship'].widget.attrs['maxlength'] = '10'
        self.fields['emergency_contact_3_phone'].widget.attrs['maxlength'] = '15'

