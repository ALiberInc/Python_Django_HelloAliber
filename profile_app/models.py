from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import MaxLengthValidator

import datetime
from datetime import timedelta

"""old
class Department(models.Model):
    #部門モデル
    dep_id = models.SmallIntegerField(primary_key=True, verbose_name='部門ID')
    department = models.CharField(verbose_name='部門', max_length=10)

    class Meta:
        verbose_name_plural = 'Department'

    def __str__(self):
        return self.department
"""

class EDepartment(models.Model):
    """部門モデル"""
    dep_id = models.AutoField(primary_key=True)
    department = models.CharField(verbose_name='部門', max_length=35)
    establish_date = models.DateTimeField(verbose_name='設立日', default=datetime.datetime.today() - timedelta(days=365 * 30 + 7))
    delete = models.IntegerField(verbose_name='削除', default=0)
    create_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    create_id = models.IntegerField(verbose_name='作成者')
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    update_id = models.IntegerField(verbose_name='更新者')

    class Meta:
        managed = False
        db_table = 'e_department'

    def __str__(self):
        return self.department

"""old
class Profile(models.Model):
    #社員情報モデル

    user_id = models.AutoField(unique=True, primary_key=True)
    id = models.ForeignKey(CustomUser, verbose_name='ユーザーID', on_delete=models.PROTECT, related_name='customer_id')
    last_name_k = models.CharField(verbose_name='姓（カタカナ）', max_length=30, blank=True)
    #last_name_k = models.CharField(verbose_name='姓（カタカナ）', validators=[MaxLengthValidator(20,'Too long name here')], max_length=30, blank=True)
    #last_name_k.validators[-1].message = 'Your question is too long.'
    first_name_k = models.CharField(verbose_name='名（カタカナ）', max_length=30, blank=True)
    last_name = models.CharField(verbose_name='姓', max_length=18)
    first_name = models.CharField(verbose_name='名', max_length=18)
    gender = models.CharField(verbose_name='性別', default='0', max_length=15)
    birth = models.DateField(verbose_name='生年月日', default=datetime.datetime.today() - timedelta(days=365 * 30 + 7))
    nationality = models.CharField(verbose_name='国籍', max_length=30, blank=True)
    phone = models.CharField(verbose_name='携帯電話', max_length=20, blank=True)
    postal_code = models.CharField(verbose_name='郵便番号', max_length=15, blank=True)
    address1 = models.CharField(verbose_name='住所1', max_length=128, blank=True)
    address2 = models.CharField(verbose_name='住所2', max_length=128, blank=True)
    residence_card = models.CharField(verbose_name='在留カード番号', max_length=20, blank=True)
    health_insurance = models.CharField(verbose_name='健康保険番号', max_length=20, blank=True)
    department_pro = models.ForeignKey(Department, verbose_name='部門', on_delete=models.SET(0),related_name='department_pro')
    emergency_contact_1_name = models.CharField(verbose_name='緊急連絡先1_名前', max_length=30, blank=True)
    emergency_contact_1_relationship = models.CharField(verbose_name='緊急連絡先1_続柄', max_length=10, blank=True)
    emergency_contact_1_phone = models.CharField(verbose_name='緊急連絡先1_電話番号', max_length=20, blank=True)
    emergency_contact_2_name = models.CharField(verbose_name='緊急連絡先2_名前', max_length=30, blank=True)
    emergency_contact_2_relationship = models.CharField(verbose_name='緊急連絡先2_続柄', max_length=10, blank=True)
    emergency_contact_2_phone = models.CharField(verbose_name='緊急連絡先2_電話番号', max_length=20, blank=True)
    emergency_contact_3_name = models.CharField(verbose_name='緊急連絡先3_名前', max_length=30, blank=True)
    emergency_contact_3_relationship = models.CharField(verbose_name='緊急連絡先3_続柄', max_length=10, blank=True)
    emergency_contact_3_phone = models.CharField(verbose_name='緊急連絡先3_電話番号', max_length=20, blank=True)
    # delete = models.BooleanField(verbose_name='削除', default=0)
    delete = models.SmallIntegerField(verbose_name='削除', default=0)
    create_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    create_id = models.CharField(verbose_name='作成者', max_length=20)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    update_id = models.CharField(verbose_name='更新者', max_length=20)

    class Meta:
        verbose_name_plural = 'Profile'

    # 　文字列でクラスを表示する
    def __str__(self):
        return self.last_name
    
    def __unicode__(self):
        return self.last_name
"""

class EProfile(models.Model):
    """社員情報モデル"""
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    last_name_k = models.CharField(verbose_name='姓（カタカナ）', max_length=30)
    first_name_k = models.CharField(verbose_name='名（カタカナ）', max_length=30)
    last_name = models.CharField(verbose_name='姓', max_length=18)
    first_name = models.CharField(verbose_name='名', max_length=18)
    gender = models.CharField(verbose_name='性別', default='0', max_length=15)
    birth = models.DateField(verbose_name='生年月日', default=datetime.datetime.today() - timedelta(days=365 * 30 + 7))
    nationality = models.CharField(verbose_name='国籍', max_length=30, blank=True)
    phone = models.CharField(verbose_name='携帯電話', max_length=20, blank=True)
    postal_code = models.CharField(verbose_name='郵便番号', max_length=15, blank=True)
    address1 = models.CharField(verbose_name='住所1', max_length=128, blank=True)
    address2 = models.CharField(verbose_name='住所2', max_length=128, blank=True)
    residence_card = models.CharField(verbose_name='在留カード番号', max_length=20, blank=True)
    health_insurance = models.CharField(verbose_name='健康保険番号', max_length=20, blank=True)
    department_pro_id = models.IntegerField()
    emergency_contact_1_name = models.CharField(verbose_name='緊急連絡先1_名前', max_length=30, blank=True)
    emergency_contact_1_relationship = models.CharField(verbose_name='緊急連絡先1_続柄', max_length=10, blank=True)
    emergency_contact_1_phone = models.CharField(verbose_name='緊急連絡先1_電話番号', max_length=20, blank=True)
    emergency_contact_2_name = models.CharField(verbose_name='緊急連絡先2_名前', max_length=30, blank=True)
    emergency_contact_2_relationship = models.CharField(verbose_name='緊急連絡先2_続柄', max_length=10, blank=True)
    emergency_contact_2_phone = models.CharField(verbose_name='緊急連絡先2_電話番号', max_length=20, blank=True)
    emergency_contact_3_name = models.CharField(verbose_name='緊急連絡先3_名前', max_length=30, blank=True)
    emergency_contact_3_relationship = models.CharField(verbose_name='緊急連絡先3_続柄', max_length=10, blank=True)
    emergency_contact_3_phone = models.CharField(verbose_name='緊急連絡先3_電話番号', max_length=20, blank=True)
    delete = models.IntegerField()
    create_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    create_id = models.IntegerField(verbose_name='作成者')
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    update_id = models.IntegerField(verbose_name='更新者')

    class Meta:
        managed = False
        db_table = 'e_profile'
        
class MList(models.Model):
    """マスターテーブル"""
    code_type = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    value = models.CharField(max_length=200)
    sort = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'm_list'
        unique_together = (('code_type', 'id'),)