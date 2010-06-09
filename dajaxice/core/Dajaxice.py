import logging

from django.conf import settings
from django.utils.importlib import import_module

log = logging.getLogger('dajaxice.DajaxiceRequest')

class DajaxiceModule(object):
    def __init__(self, module, path):
        self.path = path
        self.functions = []
        self.sub_modules = []
        
        module = module.split('.')
        self.name = module[0]
        self.add(module)
    
    def add_function(self, function):
        self.functions.append(function)
    
    def has_sub_modules(self):
        return len(self.sub_modules) > 0
        
    def add(self, module):
        if not hasattr(module,'__iter__'):
            module = module.split('.')
        
        if len(module) == 2:
            self.add_function(module[1])
        else:
            sub_module = self.exist_submodule(module[1])
            module = '.'.join(module[1:])
            
            if type(sub_module) == int:
                self.sub_modules[sub_module].add(module)
            else:
                self.sub_modules.append(DajaxiceModule(module, self.path))
        
    def exist_submodule(self, name):
        for module in self.sub_modules:
            if module.name == name:
                return self.sub_modules.index(module)
        return False
    
class Dajaxice(object):
    def __init__(self):
        self._registry = []
        self._callable = []
        
        for function in getattr(settings, 'DAJAXICE_FUNCTIONS', ()):
            function = function.rsplit('.',1)
            self.register_function(function[0],function[1])
        
    def register(self, function):
        self.register_function(function.__module__, function.__name__)
    
    def register_function(self, module, name):
        callable_function = '%s.%s' % (module, name)
        if callable_function in self._callable:
            log.warning('%s already registered as dajaxice function.' % callable_function)
            return
        
        self._callable.append(callable_function)
        
        module_without_ajax = module.replace('.ajax','')
        module = '%s.%s' % (module_without_ajax, name)
        
        exist_module = self._exist_module(module.split('.')[0])
        if type(exist_module) == int:
            self._registry[exist_module].add(module)
        else:
            self._registry.append(DajaxiceModule(module, module_without_ajax))
        
    def is_callable(self, name):
        return name in self._callable
        
    def _exist_module(self,module_name):
        for module in self._registry:
            if module.name == module_name:
                return self._registry.index(module)
        return False
        
    def get_functions(self):
        return self._registry

LOADING_DAJAXICE = False

def dajaxice_autodiscover():
    """
    Auto-discover INSTALLED_APPS ajax.py modules and fail silently when
    not present.
    NOTE: dajaxice_autodiscover was inspired/copied from django.contrib.admin autodiscover
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