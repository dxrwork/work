# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import datetime

from django.db import models


class workRecordManager(models.Manager):
    def save_record(self, data):
        """
        保存记录
        """
        try:
            workRecord.objects.create(
                no1=data.get('no1'),
                no2=data.get('no2'),
                no3=data.get('no3'),
                no4=data.get('no4'),
                appearance=data.get('appearance'),
                measure=data.get('measure'),
                operator=data.get('username'),
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception as e:
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


class workRecord(models.Model):
    """
    会议记录
    """
    no1 = models.CharField(u"专业", max_length=64)
    no2 = models.CharField(u"故障类型", max_length=64)
    no3 = models.CharField(u"故障大类", max_length=64)
    no4 = models.CharField(u"故障小类", max_length=64)
    appearance = models.TextField(u"故障现象", null=True, blank=True)
    measure = models.TextField(u"处理措施", null=True, blank=True)
    record_time = models.DateTimeField(u"记录时间", default=datetime.datetime.now)
    operator = models.CharField(u"记录人", max_length=64)
    objects = workRecordManager()

    def __unicode__(self):
        return self.no1

    class Meta:
        verbose_name = u"信息记录"
        verbose_name_plural = u"信息记录"
        db_table = 'workrecord'


# 建立城市自关联数据库表
class AreaInfo(models.Model):
     atitle = models.CharField(max_length=30)
     aParent = models.ForeignKey('self',null=True,blank=True,on_delete=models.DO_NOTHING)

     def __str__(self):
         return self.atitle

     class Meta:
         db_table = 'areas'  # 指定表名称

