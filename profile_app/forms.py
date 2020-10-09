from django import forms
from django.forms import ModelForm
from django.core.mail import EmailMessage
from .models import Profile, Department
from accounts.models import CustomUser
from django.forms import MultiWidget
import logging

logger = logging.getLogger(__name__)

class ProfileEditForm(ModelForm):
    class Meta:
        model = Profile
        fields = ("last_name", "first_name", "department_pro")


class TryUpdateForm(forms.Form):
    """ModelsFormを使わなくて、DB登録(Form)"""
    last_name = forms.CharField(label='last_name', max_length=30)
    first_name = forms.CharField(label='first_name', max_length=30)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # col-widget
        self.fields['last_name'].widget.attrs['class'] = 'form-control col-15'
        self.fields['first_name'].widget.attrs['class'] = 'form-control col-15'

    def clean(self):
        return self.cleaned_data

    def save(self, request):
        request.last_name = self.data.get('last_name')
        request.first_name = self.data.get('first_name')
        return request

