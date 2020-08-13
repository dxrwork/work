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

from django.shortcuts import render
from django.http import HttpResponse
import json
from home_application.models import workRecord

# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, 'home_application/index_home.html')


def dev_guide(request):
    """
    开发指引
    """
    return render(request, 'home_application/dev_guide.html')


def contact(request):
    """
    联系页
    """
    return render(request, 'home_application/contact.html')

def helloworld(request):
    return render(request, 'home_application/helloworld.html')


def render_json(res_dict):
    return HttpResponse(json.dumps(res_dict), content_type='application/json')


# 输入值提交请求
def say_hello(request):
    data = request.POST.get('input', None)
    data = 'Congratulations!'if data == 'Hello' else 'Try input Hello'
    res = {'data': data}
    return render_json(res)

def meeting(request):
    return render(request, 'home_application/meeting.html')

def save_record(request):
    """
    保存数据
    """
    theme = request.POST.get('theme', '')
    content = request.POST.get('content', '')

    data = {
        'theme': theme,
        'content': content,
        'username': request.user.username,
    }
    result = workRecord.objects.save_record(data)

    return render_json(result)


def records(request):
    """
    查询记录
    """
    record_list = workRecord.objects.all().order_by('id')
    data = []
    for index, record in enumerate(record_list):
        data.append({
            'index': index,
            'theme': record.theme,
            'content': record.content,
        })
    return render_json({'code': 0, 'message': 'success', 'data': data})

def chaxun(request):
    return render(request, 'home_application/chaxun.html')