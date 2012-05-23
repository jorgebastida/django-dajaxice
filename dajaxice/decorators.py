import functools

from dajaxice.core import dajaxice_functions


def dajaxice_register(*dargs, **dkwargs):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            return function(request, *args, **kwargs)
        dajaxice_functions.register(function, *dargs, **dkwargs)
        return wrapper
    return decorator
