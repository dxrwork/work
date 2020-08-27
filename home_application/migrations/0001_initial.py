# Generated by Django 2.2.6 on 2020-08-25 14:47

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='workRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no1', models.CharField(max_length=64, verbose_name='专业')),
                ('no2', models.CharField(max_length=64, verbose_name='故障类型')),
                ('no3', models.CharField(max_length=64, verbose_name='故障大类')),
                ('no4', models.CharField(max_length=64, verbose_name='故障小类')),
                ('appearance', models.TextField(blank=True, null=True, verbose_name='故障现象')),
                ('measure', models.TextField(blank=True, null=True, verbose_name='处理措施')),
                ('record_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='记录时间')),
                ('operator', models.CharField(max_length=64, verbose_name='记录人')),
            ],
            options={
                'verbose_name': '信息记录',
                'verbose_name_plural': '信息记录',
                'db_table': 'workrecord',
            },
        ),
        migrations.CreateModel(
            name='AreaInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atitle', models.CharField(max_length=30)),
                ('aParent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home_application.AreaInfo')),
            ],
            options={
                'db_table': 'areas',
            },
        ),
    ]
