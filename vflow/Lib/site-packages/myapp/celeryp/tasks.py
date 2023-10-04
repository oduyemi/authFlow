'''
Created on Nov 26, 2020

@author: roman.schroeder
'''

from .worker import app


@app.task
def add(x, y):
    return x + y