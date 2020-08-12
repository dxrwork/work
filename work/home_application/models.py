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
        保存会议记录
        """
        try:
            workRecord.objects.create(
                theme=data.get('theme'),
                content=data.get('content'),
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
    theme = models.CharField(u"会议主题", max_length=64)
    content = models.TextField(u"会议内容", null=True, blank=True)
    record_time = models.DateTimeField(u"会议时间", default=datetime.datetime.now)
    operator = models.CharField(u"记录人", max_length=64)
    objects = workRecordManager()

    def __unicode__(self):
        return self.theme

    class Meta:
        verbose_name = u"会议记录"
        verbose_name_plural = u"会议记录"




class HostModelManager(models.Manager):
    def to_dict(self):
        qs = super().get_queryset()
        res_dict = [{
            'input1':item.zhuti,
            'input2':item.neirong
        }for item in qs]
        return res_dict

class HostModel(models.Model):
    zhuti = models.CharField(max_length=30,verbose_name='主题')
    neirong = models.CharField(max_length=100,verbose_name='内容')

    objects = HostModelManager()