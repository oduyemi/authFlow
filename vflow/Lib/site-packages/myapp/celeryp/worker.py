#!/usr/bin/env python
# -*- coding: utf-8 -*-
# myapp.celeryp.app
'''
:author:    roman-telepathy-ai
:contact:   roman.schroeder(at)telepathy.ai
:copyright: Copyright 2020, Telepathy Labs

myapp.celeryp.app
---------
Module
'''

from __future__ import absolute_import

import celery

from .config import BROKER_CONN_URI, BACKEND_CONN_URI

VERSION = (0, 1, 0)

__all__ = []
__author__ = 'roman-telepathy-ai <roman.schroeder(at)telepathy.ai>'
__version__ = '.'.join(str(x) for x in VERSION)
__copyright__ = 'Copyright 2020, Telepathy Labs'


app = celery.Celery(__name__, broker=BROKER_CONN_URI, backend=BACKEND_CONN_URI)
