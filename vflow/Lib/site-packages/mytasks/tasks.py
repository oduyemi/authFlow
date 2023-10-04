'''
Created on Nov 26, 2020

@author: roman.schroeder
'''

# from __future__ import absolute_import
# 
# import celery
# import redis
# 
# # from .worker import app
# from .worker import addtask
# 
# # @app.task
# 
# 
# #@celery.shared_task
# # def add(x, y):
# #     return x + y
# 
# 
# class CustomTask(celery.Task):
#     def run(self, x, y):
#         return x + y
# 
# 
# 
# class MyTasks(object):
#     def add(self, x, y):
#         return x + y
#     def add_one(self, x):
#         return x + 1
#     def add_two(self, x):
#         return x + 2
# 
# 
# def main():
#     pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
#     r = redis.Redis(connection_pool=pool)
#     print(r.keys())
#     #add = CustomTask()
#     #
#     result = addtask.delay(1, 3)
#     print()
#     print(result.ready())
#     print(result.result)
#     print(result.task_id)
#     print(result.get())
#     #
#     print(result.forget())
#     print(r.keys())
# 
# 
# # if __name__ == '__main__':
# #     main()