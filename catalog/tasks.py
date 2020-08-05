# Create your tasks here
from __future__ import absolute_import, unicode_literals
from datetime import timedelta
from time import sleep

from celery import shared_task
from celery.task import periodic_task
from celery.schedules import crontab

from catalog.models import GoodItem

# @periodic_task(run_every=(crontab(minute='*/1')), name='my_task_name')
@periodic_task(run_every=(timedelta(seconds=10)), name='my_task_name_1')
def my_task_1():
    print('my_task_print_1')
    return 'my_task_return_1'

@periodic_task(run_every=(timedelta(seconds=10)), name='my_task_name_2')
def my_task_2():
    print('my_task_print_2')
    return 'my_task_return_2'

@periodic_task(run_every=(timedelta(seconds=10)), name='sleep20')
def my_task_20():
    print('my_task_print sleep20 start')
    sleep(20)
    print('my_task_print sleep20 stop')
    return 'my_task_return'

@periodic_task(run_every=(timedelta(seconds=10)), name='sleep30')
def my_task_30():
    print('my_task_print sleep30 start')
    sleep(20)
    print('my_task_print sleep30 stop')
    return 'my_task_return'

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_products():
    return GoodItem.objects.count()


@shared_task
def rename_product(product_id, title):
    product = GoodItem.objects.get(id=product_id)
    product.title = title
    product.save()