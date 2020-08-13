# -*- coding: utf-8 -*-

from common.mymako import render_mako_context
from blueking.component.shortcuts import get_client_by_request
from home_application.celery_tasks import async_task, execute_task, get_time


def home(request):
    """
    首页
    """
    # 调用自己开发的API组件
    client = get_client_by_request(request)
    kwargs = {'token': '@adf*adsd^'}
    resp = client.cm.get_capacity(**kwargs)

    # 执行celery异步任务
    # async_task.delay(1, 2, 1)

    # 执行定时任务
    # execute_task(2)
    return render_mako_context(request, '/home_application/home.html', {'result': resp})


def test(request):
    """
    开发指引
    """
    data = {
        'data1': 11,
        'data2': 22,
    }
    return render_mako_context(request, '/home_application/test.html', {'data': data})


def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')


def helloworld(request):
    """
    helloworld
    """
    return render_mako_context(request, '/home_application/helloworld.html')
