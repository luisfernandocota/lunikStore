# -*- coding:utf-8 -*-
from django.apps import apps

from celery import shared_task

#-- Call Tasks:
# task_test_task.delay(params)

@shared_task
def task_test_task(params):
    pass
