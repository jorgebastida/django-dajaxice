from django.utils import simplejson
from dajaxice.core import dajaxice_functions


def complex_example1(request):
    return simplejson.dumps({'message': 'hello world'})

dajaxice_functions.register(complex_example1)


def complex_example2(request):
    return simplejson.dumps({'numbers': [1, 2, 3]})

dajaxice_functions.register(complex_example2)
