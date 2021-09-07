# Generated by Django 3.1.1 on 2021-04-14 05:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('asset_id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='資産番号')),
                ('model_name', models.CharField(blank=True, max_length=50, verbose_name='モデル名')),
                ('storing_date', models.DateField(default=datetime.datetime(1991, 4, 15, 5, 39, 51, 436339), verbose_name='入庫日')),
                ('purchase_date', models.DateField(default=datetime.datetime(1991, 4, 15, 5, 39, 51, 436368), verbose_name='購入日')),
                ('serial_number', models.CharField(blank=True, max_length=50, verbose_name='識別番号')),
                ('delete', models.SmallIntegerField(default=0, verbose_name='削除')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('create_id', models.CharField(max_length=20, verbose_name='作成者')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('update_id', models.CharField(max_length=20, verbose_name='更新者')),
            ],
            options={
                'verbose_name_plural': 'Asset',
                'db_table': 'asset',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False, verbose_name='品名ID')),
                ('product_name', models.CharField(blank=True, max_length=50, verbose_name='品名')),
                ('product_abbreviation', models.CharField(blank=True, max_length=50, verbose_name='略称')),
                ('delete', models.SmallIntegerField(default=0, verbose_name='削除')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('create_id', models.CharField(max_length=20, verbose_name='作成者')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('update_id', models.CharField(max_length=20, verbose_name='更新者')),
            ],
            options={
                'verbose_name_plural': 'Product',
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Asset_History',
            fields=[
                ('asset_history_id', models.AutoField(primary_key=True, serialize=False, verbose_name='資産履歴番号')),
                ('status', models.IntegerField(choices=[(0, '入庫済'), (1, '返却済'), (2, '修理済'), (3, '貸出済'), (4, '修理依頼済'), (5, '使用不可')])),
                ('user_id', models.IntegerField(verbose_name='社員番号')),
                ('repair_reason', models.CharField(blank=True, max_length=200, verbose_name='修理理由')),
                ('delete', models.SmallIntegerField(default=0, verbose_name='削除')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='作成日時')),
                ('create_id', models.CharField(max_length=20, verbose_name='作成者')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='更新日時')),
                ('update_id', models.CharField(max_length=20, verbose_name='更新者')),
                ('asset_ash_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='asset_ash_id', to='asset_app.asset', verbose_name='資産番号')),
            ],
            options={
                'verbose_name_plural': 'Asset_History',
                'db_table': 'asset_history',
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='product_ass_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_ass_id', to='asset_app.product', verbose_name='品名ID'),
        ),
    ]