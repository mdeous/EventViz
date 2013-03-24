# -*- coding: utf-8 -*-

from copy import copy
from functools import wraps
from time import time


class cache(object):
    def __init__(self, timeout=120):
        self.timeout = timeout
        self.last_call_time = None
        self.last_retval = None
        self.last_args = []
        self.last_kwargs = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if (args == self.last_args) and (kwargs == self.last_kwargs):
                if (self.last_call_time is not None) and (time()-self.last_call_time < self.timeout):
                    return copy(self.last_retval)
            self.last_call_time = time()
            self.last_args = args
            self.last_kwargs = kwargs
            self.last_retval = func(*args, **kwargs)
            return copy(self.last_retval)
        return wrapper
