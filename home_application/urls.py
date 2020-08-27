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

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.home),
    url(r'^dev-guide/$', views.dev_guide),
    url(r'^contact/$', views.contact),
    url(r'^ebase/$', views.ebase),
    url(r'^save_record/$', views.save_record),
    url(r'^records/$', views.records),
    url(r'^export_excel/$', views.export_excel),
    url(r'^excel_upload/$', views.excel_upload),
    url(r'^search/$', views.search),
    url(r'^getNo1/$', views.getNo1),
    url(r'^getNo2/$', views.getNo2),
    url(r'^getNo3/$', views.getNo3),
    url(r'^getNo4/$', views.getNo4),
    url(r'^research/$', views.research),
    url(r'^export/$', views.export),
)
