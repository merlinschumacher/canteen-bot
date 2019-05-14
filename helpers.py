#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps
def with_logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job %s' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper