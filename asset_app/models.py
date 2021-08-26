from django.db import close_old_connections, models
import datetime
from datetime import timedelta
from accounts.models import CustomUser

# Create your models here.
class Product(models.Model):
    """品名モデル"""
    
    product_id = models.AutoField(primary_key=True, verbose_name='品名ID')
    product_name = models.CharField(verbose_name='品名', max_length=55, blank=True)
    product_abbreviation = models.CharField(verbose_name='略称', max_length=55, blank=True)
    delete = models.SmallIntegerField(verbose_name='削除', default=0)
    create_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    create_id = models.CharField(verbose_name='作成者', max_length=20)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    update_id = models.CharField(verbose_name='更新者', max_length=20)

    class Meta:
        db_table = 'product'
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.product_name

class EProduct(models.Model):
    """品名モデル"""
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_abbreviation = models.CharField(max_length=50)
    delete = models.IntegerField()
    create_date = models.DateTimeField()
    create_id = models.IntegerField()
    update_date = models.DateTimeField()
    update_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'e_product'

class Asset(models.Model):
    """資産情報モデル"""

    asset_id = models.CharField(primary_key=True, verbose_name='資産番号', max_length=100)
    num = models.IntegerField(verbose_name='NO',default=0)
    product_ass_id = models.ForeignKey(Product, verbose_name='品名', on_delete= models.PROTECT,related_name= 'product_ass_id')
    model_name = models.CharField(verbose_name='モデル名',max_length=55, blank=True)
    storing_date = models.DateField(verbose_name='入庫日', default=datetime.datetime.today() - timedelta(days=365 * 30 + 7))
    purchase_date = models.DateField(verbose_name='購入日', default=datetime.datetime.today() - timedelta(days=365 * 30 + 7))
    serial_number = models.CharField(verbose_name='識別番号', max_length=120, blank=True)
    delete = models.SmallIntegerField(verbose_name='削除', default=0)
    create_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    create_id = models.CharField(verbose_name='作成者', max_length=20)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    update_id = models.CharField(verbose_name='更新者', max_length=20)

    class Meta:
        db_table = 'asset'
        verbose_name_plural = 'Asset'

    def __str__(self):
        return self.asset_id

class EAsset(models.Model):
    """資産情報モデル"""
    asset_id = models.CharField(primary_key=True, max_length=100)
    num = models.IntegerField()
    product_ass_id = models.IntegerField()
    model_name = models.CharField(max_length=50)
    storing_date = models.DateTimeField()
    purchase_date = models.DateTimeField()
    serial_number = models.CharField(max_length=50)
    delete = models.IntegerField()
    create_date = models.DateTimeField()
    create_id = models.IntegerField()
    update_date = models.DateTimeField()
    update_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'e_asset'

class Asset_History(models.Model):
    """資産ライフサイクルモデル"""
    
    choice_area=(
        (0,'入庫済'),
        (1,'返却済'),
        (2,'修理済'),
        (3,'貸出済'),
        (4,'修理依頼済'),
        (5,'使用不可'),
        )

    asset_history_id = models.AutoField(primary_key=True, verbose_name='資産履歴番号')
    asset_ash_id = models.ForeignKey(Asset, verbose_name='資産番号', on_delete= models.PROTECT, related_name= 'asset_ash_id')
    status = models.IntegerField(choices= choice_area)
    user_id = models.IntegerField(verbose_name='社員番号', null=True)
    repair_reason = models.CharField(verbose_name='修理理由', max_length=200, blank=True, null=True)
    delete = models.SmallIntegerField(verbose_name='削除', default=0)
    create_date = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    create_id = models.CharField(verbose_name='作成者', max_length=20)
    update_date = models.DateTimeField(verbose_name='更新日時', auto_now=True)
    update_id = models.CharField(verbose_name='更新者', max_length=20)

    class Meta:
        db_table = 'asset_history'
        verbose_name_plural = 'Asset_History'

    def __str__(self):
        return self.repair_reason

class EAssetHistory(models.Model):
    """資産ライフサイクルモデル"""
    asset_history_id = models.AutoField(primary_key=True)
    asset_ash_id = models.CharField(max_length=100)
    status = models.IntegerField()
    user_id = models.IntegerField(blank=True, null=True)
    repair_reason = models.CharField(max_length=200, blank=True, null=True)
    delete = models.IntegerField()
    create_date = models.DateTimeField()
    create_id = models.IntegerField()
    update_date = models.DateTimeField()
    update_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'e_asset_history'
        