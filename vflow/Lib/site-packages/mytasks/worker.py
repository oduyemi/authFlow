'''
Created on Nov 26, 2020

@author: roman.schroeder
'''

from __future__ import absolute_import

import inspect

import celery
import redis

# app = celery.Celery(
#     __name__,
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/0',
#     # include=['mytasks.tasks']
# )

# from .tasks import CustomTask
# 
# addtask = app.register_task(CustomTask)
# 
# print(addtask)


class MulTasks(object):
    def add(self, x, y):
        return x + y
    def add_one(self, x):
        return x + 1
    def add_two(self, x):
        return x + 2
    def mul(self, x, y):
        return x * y


def make_app():
    return celery.Celery(
        __name__,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        # include=['mytasks.tasks']
    )


def get_app(*tasks, bind=True):
    app = celery.Celery(
        __name__,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0',
        # include=['mytasks.tasks']
    )
    for task in tasks:
        print(task)
        for name, m in inspect.getmembers(task, lambda x: inspect.isfunction(x) or inspect.ismethod(x)):
            print('>', name, m)
            print(dir(m))
            print(m.__annotations__)
            setattr(task, name, app.task(m, bind=bind))
            print(getattr(task, name))

#     class _MultiplyTasks(object):
#         @app.task(bind=True)
#         def mul(self, x, y):
#             return x * y
    # raise
    return app


the_app_not_to_use = get_app(MulTasks)


# @app.task
# def add(x, y):
#     return x + y


# class MyTasks(object):
# #     @app.task
# #     def add(self, x, y):
# #         return x + y
#     @app.task(bind=True)
#     def add_one(self, x):
#         return x + 1
#     @app.task(bind=True)
#     def add_two(self, x):
#         return x + 2
