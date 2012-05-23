import logging

from django.utils.importlib import import_module

log = logging.getLogger('dajaxice')


class DajaxiceFunction(object):

    def __init__(self, function, name, method):
        self.function = function
        self.name = name
        self.method = method

    def call(self, *args, **kwargs):
        return self.function(*args, **kwargs)


class DajaxiceModule(object):

    def __init__(self, name=None):
        self.name = name
        self.functions = {}
        self.submodules = {}

    def add(self, name, function):
        if '.' in name:
            module, extra = name.split('.', 1)
            if module not in self.submodules:
                self.submodules[module] = DajaxiceModule(module)
            self.submodules[module].add(extra, function)
        else:
            self.functions[name] = function


class Dajaxice(object):

    def __init__(self):
        self._registry = {}

    def register(self, function, name=None, method='POST'):

        method = self.__clean_method(method)

        # Generate a default name
        if not name:
            module = ''.join(str(function.__module__).rsplit('.ajax', 1))
            name = '.'.join((module, function.__name__))

        if ':' in name:
            log.error('Ivalid function name %s.' % name)
            return

        # Check for already registered functions
        if name in self._registry:
            log.error('%s was already registered.' % name)
            return

        # Create the dajaxice function.
        function = DajaxiceFunction(function=function,
                                    name=name,
                                    method=method)

        # Register this new ajax function
        self._registry[name] = function

    def is_callable(self, name):
        return name in self._registry

    def __clean_method(self, method):
        method = method.upper()
        if method not in ['GET', 'POST']:
            method = 'POST'
        return method

    def get(self, name):
        return self._registry[name]

    @property
    def modules(self):
        modules = DajaxiceModule()
        for name, function in self._registry.items():
            modules.add(name, function)
        return modules

LOADING_DAJAXICE = False


def dajaxice_autodiscover():
    """
    Auto-discover INSTALLED_APPS ajax.py modules and fail silently when
    not present. NOTE: dajaxice_autodiscover was inspired/copied from
    django.contrib.admin autodiscover
    """
    global LOADING_DAJAXICE
    if LOADING_DAJAXICE:
        return
    LOADING_DAJAXICE = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:

        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('ajax', app_path)
        except ImportError:
            continue

        import_module("%s.ajax" % app)

    LOADING_DAJAXICE = False
