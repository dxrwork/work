# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime
import time

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger


@task()
def async_task(x, y, type):
    """
    定义一个 celery 异步任务
    """
    time.sleep(10)
    if type == 1:
        logger.error(u"home celery 异步任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    elif type == 2:
        now = datetime.datetime.now()
        logger.error(u"home celery 定时任务执行，当前时间：{}".format(now))
    return x + y


def execute_task(type):
    """
    执行 celery 定时任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute, type], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/1', hour='*', day_of_week="*")：每 1 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    now = datetime.datetime.now()
    logger.error(u"home celery 周期任务调用成功，当前时间：{}".format(now))
