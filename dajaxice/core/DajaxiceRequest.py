#----------------------------------------------------------------------
# Copyright (c) 2009 Benito Jorge Bastida
# All rights reserved.
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#    o Redistributions of source code must retain the above copyright
#      notice, this list of conditions, and the disclaimer that follows.
#
#    o Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions, and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
#    o Neither the name of Digital Creations nor the names of its
#      contributors may be used to endorse or promote products derived
#      from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY DIGITAL CREATIONS AND CONTRIBUTORS *AS
#  IS* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL DIGITAL
#  CREATIONS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
#  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
#  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
#  DAMAGE.
#----------------------------------------------------------------------

import os
import sets
import logging
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson


from dajaxice.exceptions import FunctionNotCallableError

# Python 2.7 has an importlib with import_module; for older Pythons,
# Django's bundled copy provides it.
try:
    from importlib import import_module
    DAJAXICE_MODERN_IMPORT = True
except:
    try:
        from django.utils import importlib
        DAJAXICE_MODERN_IMPORT = True
    except:
        DAJAXICE_MODERN_IMPORT = False

logging.info('DAJAXICE DAJAXICE_MODERN_IMPORT=%s' % DAJAXICE_MODERN_IMPORT)

def safe_dict(d): 
    """
    Recursively clone json structure with UTF-8 dictionary keys
    http://www.gossamer-threads.com/lists/python/bugs/684379
    """
    if isinstance(d, dict): 
        return dict([(k.encode('utf-8'), safe_dict(v)) for k,v in d.iteritems()]) 
    elif isinstance(d, list): 
        return [safe_dict(x) for x in d] 
    else: 
        return d
                        
class DajaxiceRequest(object):
    
    def __init__(self, request, call):
        call = call.split('.')
        self.app_name = call[0]
        self.method = call[1]
        self.request = request
        
        self.project_name = os.environ['DJANGO_SETTINGS_MODULE'].split('.')[0]
        self.module = "%s.ajax" % self.app_name
        self.full_name = "%s.%s" % (self.module,self.method,)
        
    @staticmethod
    def get_js_functions():
        functions = [fun.split('.') for fun in DajaxiceRequest.get_functions()]
        modules = [fun[0] for fun in functions]
        modules = list(sets.Set(modules))
        data = {}
        for module in modules:
            data[module] = []
            for function in functions:
                if function[0] == module:
                    data[module].append(function[2])
        return data
        
    @staticmethod
    def get_media_prefix():
        return getattr(settings, 'DAJAXICE_MEDIA_PREFIX', "dajaxice")
        
    @staticmethod
    def get_functions():
        return getattr(settings, 'DAJAXICE_FUNCTIONS', ())
    
    @staticmethod
    def get_debug():
        return getattr(settings, 'DAJAXICE_DEBUG', True )
    
    @staticmethod
    def get_cache_control():
        if settings.DEBUG:
            return 0
        return getattr(settings, 'DAJAXICE_CACHE_CONTROL', 5 * 24 * 60 * 60 )
    
    @staticmethod
    def get_exception_message():
        return getattr(settings, 'DAJAXICE_EXCEPTION_MESSAGE', "'DAJAXICE_EXCEPTION'")
    
    def _is_callable(self):
        """
        Return if the request function was registered.
        """
        return self.full_name in settings.DAJAXICE_FUNCTIONS
        
    def _get_ajax_function(self):
        """
        Return a callable ajax function.
        This function should be imported according the Django version.
        """
        if DAJAXICE_MODERN_IMPORT:
            return self._modern_get_ajax_function()
        else:
            return self._old_get_ajax_function()
    
    def _old_get_ajax_function(self):
        """
        Return a callable ajax function.
        This function doesn't uses django.utils.importlib
        """
        
        self.module_import_name = "%s.%s" % ( self.project_name, self.module)   
        try:
            return self._old_import()
        except:
            self.module_import_name = self.module
            return self._old_import()
    
    def _old_import(self):
        """
        Import this.module_import_name 
        This function doesn't uses django.utils.importlib
        """
        mod = __import__(self.module_import_name , None, None, [self.method])
        return mod.__getattribute__(self.method)
        
    def _modern_get_ajax_function(self):
        """
        Return a callable ajax function.
        This function uses django.utils.importlib
        """
        self.module_import_name = "%s.%s" % ( self.project_name, self.module )
        try:
            return self._modern_import()
        except:
            self.module_import_name = self.module
            return self._modern_import()
    
    def _modern_import(self):
        from django.utils import importlib
        mod = importlib.import_module(self.module_import_name)
        return mod.__getattribute__(self.method)
    
    def _print_exception(self,e):
        import traceback
        print ""
        print "#"*60
        print "uri:      %s" % self.request.build_absolute_uri()
        print "function: %s" % self.full_name
        print "#"*60
        print ""
        traceback.print_exc(e)
        print ""
        
    def process(self):
        """
        Process the dajax request calling the apropiate method.
        """
        if self._is_callable():
            logging.debug('DAJAXICE Function %s is callable' % self.full_name)
            callback = self.request.POST.get('callback')
            try:
                argv = simplejson.loads(self.request.POST.get('argv'))
                argv = safe_dict(argv)
            except:
                argv = []
            logging.debug('DAJAXICE Callback %s' % callback)
            try:
                #1. get the function
                thefunction = self._get_ajax_function()
                #2. call the function
                response = '%s(%s)' % ( callback, thefunction(self.request, **argv) )
                
            except Exception, e:
                logging.error('DAJAXICE Exception %s' % str(e))
                if DajaxiceRequest.get_debug():
                    self._print_exception(e)
                    
                response = '%s(%s)' % ( callback, DajaxiceRequest.get_exception_message())
            logging.info('DAJAXICE response: %s' % response)
            return HttpResponse(response, mimetype="application/x-json")
            
        else:
            logging.debug('DAJAXICE Function %s is not callable' % self.full_name)
            raise FunctionNotCallableError(name=self.full_name)
