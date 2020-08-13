# -*- coding: utf-8 -*-

# import from apps here


# import from lib
# ===============================================================================
from django.contrib import admin
from get_capacity.models import TaskLog, TaskResult, CapacityData

admin.site.register(CapacityData)
# admin.site.register(TaskResult)
# admin.site.register(TaskLog)
# ===============================================================================
