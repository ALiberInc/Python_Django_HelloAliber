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

class ProfileCreateForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ("user", "created_at", "updated_at")
