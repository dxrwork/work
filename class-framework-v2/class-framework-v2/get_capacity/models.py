# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from common.log import logger


class CapacityDataManager(models.Manager):
    def save_data(self, data):
        """
        保存执行结果数据
        """
        try:
            CapacityData.objects.create(
                ip=data[6],
                filesystem=data[0],
                size=data[1],
                used=data[2],
                avail=data[3],
                use=data[4],
                mounted=data[5],
                createtime=datetime.now()
            )
            result = {'result': True, 'message': u"保存成功"}
        except Exception as e:
            logger.error(u"save_data %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


class CapacityData(models.Model):
    """
    存储查询的容量数据
    """
    ip = models.CharField('ip', max_length=64, blank=True, null=True)
    filesystem = models.CharField('filesystem', max_length=64)
    size = models.CharField('size', max_length=64)
    used = models.CharField('used', max_length=64)
    avail = models.CharField('avail', max_length=64)
    use = models.CharField('Use%', max_length=64)
    mounted = models.TextField('mounted', max_length=64)
    createtime =  models.DateTimeField(u"保存时间")
    objects = CapacityDataManager()

    
    def __unicode__(self):
        return self.filesystem

    class Meta:
        verbose_name = u"磁盘容量数据"
        verbose_name_plural = u"磁盘容量数据"





class TaskLogManager(models.Manager):
    def save_log(self, datalist):
        """
        保存执行结果数据
        """
        try:
            for data in datalist:
                TaskLog.objects.create(
                    operator=data.get('operator'),
                    starttime=data.get('starttime'),
                    endtime=data.get('endtime'),
                    log=data.get('log'),
                    ip=data.get('ip'),
                    result=data.get('result'),
                    stepname=data.get('stepname'),
                )
            result = {'result': True, 'message': u"保存成功"}
        except Exception as e:
            logger.error(u"save_log： %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result


# 定义表，存储执行历史
class TaskLog(models.Model):
    """
    执行历史日志
    """
    operator = models.CharField(u"操作人", max_length=64)
    starttime = models.DateTimeField(u"起始执行时间")
    endtime = models.DateTimeField(u"结束执行时间")
    log = models.TextField(u"执行日志", blank=True, null=True)
    ip = models.IPAddressField(u"执行IP")
    result = models.CharField(u"执行结果", max_length=64)
    stepname = models.CharField(u"步骤名", max_length=64)
    objects = TaskLogManager()

    
    def __unicode__(self):
        return self.operator

    class Meta:
        verbose_name = u"执行历史日志"
        verbose_name_plural = u"执行历史日志"


# 串行任务结果保存
class TaskResultManager(models.Manager):
    def save_result(self, datalist):
        """
        保存会议记录
        """
        try:
            for data in datalist:
                TaskResult.objects.create(
                    func=data.get('func'),
                    result=data.get('result'),
                )
            result = {'result': True, 'message': u"保存成功"}
        except Exception as e:
            logger.error(u"save_result %s" % e)
            result = {'result': False, 'message': u"保存失败, %s" % e}
        return result
    

class TaskResult(models.Model):
    """
    任务执行结果
    """
    # taskid = models.DateTimeField(u"任务时间戳")
    func = models.CharField(u"执行函数", max_length=64)
    result = models.TextField(u"函数返回结果", max_length=64)
    objects = TaskResultManager()

    
    def __unicode__(self):
        return self.func

    class Meta:
        verbose_name = u"任务执行结果"
        verbose_name_plural = u"任务执行结果"