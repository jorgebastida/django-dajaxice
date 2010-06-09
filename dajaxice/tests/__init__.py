#----------------------------------------------------------------------
# Copyright (c) 2009-2010 Benito Jorge Bastida
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
import unittest

from django.test import TestCase
from django.conf import settings

from dajaxice.exceptions import FunctionNotCallableError, DajaxiceImportError
from dajaxice.core import DajaxiceRequest
from dajaxice.core.DajaxiceRequest import DAJAXICE_MODERN_IMPORT
from dajaxice.core.Dajaxice import Dajaxice, DajaxiceModule
from dajaxice.core import dajaxice_functions

class DjangoIntegrationTest(TestCase):
    
    urls = 'dajaxice.tests.urls'
    
    def setUp(self):
        settings.DAJAXICE_MEDIA_PREFIX = "dajaxice"
        settings.DAJAXICE_DEBUG = False
        settings.INSTALLED_APPS += ('dajaxice.tests',)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'dajaxice'
        
    def test_calling_not_registered_function(self):
        self.failUnlessRaises(FunctionNotCallableError,self.client.post, '/dajaxice/dajaxice.tests.this_function_not_exist/',{'callback':'my_callback'})

    def test_calling_registered_function(self):
        response = self.client.post('/dajaxice/dajaxice.tests.test_foo/',{'callback':'my_callback'})

        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content,'my_callback()')

    def test_calling_registered_function_with_params(self):
        
        response = self.client.post('/dajaxice/dajaxice.tests.test_foo_with_params/',{'callback':'my_callback', 'argv': '{"param1":"value1"}'})
        
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content,'my_callback("value1")')
        
    def test_bad_function(self):
        
        response = self.client.post('/dajaxice/dajaxice.tests.test_ajax_exception/',{'callback':'my_callback'})
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content,"my_callback('DAJAXICE_EXCEPTION')")
    
    def test_is_callable(self):
        
        dr = DajaxiceRequest(None, 'dajaxice.tests.test_registered_function')
        self.failUnless(dr._is_callable())
        
        dr = DajaxiceRequest(None, 'dajaxice.tests.test_ajax_not_registered')
        self.failIf(dr._is_callable())
        
    def test_get_js_functions(self):
        
        js_functions = DajaxiceRequest.get_js_functions()
        
        callables = ['dajaxice.tests.ajax.test_registered_function',
                    'dajaxice.tests.ajax.test_string',
                    'dajaxice.tests.ajax.test_ajax_exception',
                    'dajaxice.tests.ajax.test_foo',
                    'dajaxice.tests.ajax.test_foo_with_params']
        
        functions = [f.rsplit('.',1)[1] for f in callables]
        
        self.failUnlessEqual(len(js_functions), 1)
        self.failUnlessEqual(dajaxice_functions._callable, callables)
        
        sub = js_functions[0]
        self.failUnlessEqual(len(sub.sub_modules), 1)
        self.failUnlessEqual(len(sub.functions), 0)
        self.failUnlessEqual(sub.name, 'dajaxice')
        
        sub = js_functions[0].sub_modules[0]
        self.failUnlessEqual(len(sub.sub_modules), 0)
        self.failUnlessEqual(len(sub.functions), 5)
        self.failUnlessEqual(sub.functions, functions)
        self.failUnlessEqual(sub.name, 'tests')

    def test_get_ajax_function(self):
        
        # Test modern Import with a real ajax function
        dr = DajaxiceRequest(None, 'dajaxice.tests.test_foo')
        function = dr._modern_get_ajax_function()
        self.failUnless(hasattr(function, '__call__') )
        
        # Test old Import with a real ajax function
        dr = DajaxiceRequest(None, 'dajaxice.tests.test_foo')
        function = dr._old_get_ajax_function()
        self.failUnless(hasattr(function, '__call__') )
        
        # Test modern Import without a real ajax function
        dr = DajaxiceRequest(None, 'dajaxice.tests.test_foo2')
        self.failUnlessRaises(DajaxiceImportError, dr._modern_get_ajax_function)
        
        # Test old Import without a real ajax function
        dr = DajaxiceRequest(None, 'dajaxice.tests.test_foo2')
        self.failUnlessRaises(DajaxiceImportError, dr._old_get_ajax_function)


class DajaxiceModuleTest(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_constructor(self):
        dajaxice = DajaxiceModule('a.b.c.d.function','a.b.c.d.function')
        self.failUnlessEqual(dajaxice.name, 'a')
        self.failUnlessEqual(len(dajaxice.sub_modules), 1)
        self.failUnlessEqual(len(dajaxice.functions), 0)
        
        sub = dajaxice.sub_modules[0]
        self.failUnlessEqual(sub.name, 'b')
        self.failUnlessEqual(len(sub.sub_modules), 1)
        self.failUnlessEqual(len(sub.functions), 0)
        
        sub = sub.sub_modules[0]
        self.failUnlessEqual(sub.name, 'c')
        self.failUnlessEqual(len(sub.sub_modules), 1)
        self.failUnlessEqual(len(sub.functions), 0)
        
        sub = sub.sub_modules[0]
        self.failUnlessEqual(sub.name, 'd')
        self.failUnlessEqual(len(sub.sub_modules), 0)
        self.failUnlessEqual(len(sub.functions), 1)
        self.failUnlessEqual(sub.functions, ['function'])
    
    def test_add_function(self):
        dajaxice = DajaxiceModule('a.function','a.function')
        dajaxice.add_function('function2')
        self.failUnlessEqual(dajaxice.functions, ['function','function2'])
    
    def test_has_sub_modules(self):
        dajaxice = DajaxiceModule('a.function','a.function')
        self.assertFalse(dajaxice.has_sub_modules())
        
        dajaxice = DajaxiceModule('a.b.function','a.b.function')
        self.assertTrue(dajaxice.has_sub_modules())
    
    def test_exist_submodule(self):
        dajaxice = DajaxiceModule('a.b.function','a.b.function')
        self.assertFalse(dajaxice.exist_submodule('c'))
        
        self.failUnlessEqual(type(dajaxice.exist_submodule('b')), int)
        self.failUnlessEqual(dajaxice.exist_submodule('b'), 0)

class DajaxiceModuleTest(unittest.TestCase):
    def setUp(self):
        self.dajaxice = Dajaxice()
        
    def test_is_callable(self):
        self.dajaxice._callable.append('test')
        
        self.assertTrue(self.dajaxice.is_callable('test'))
        self.assertFalse(self.dajaxice.is_callable('other'))
    
    def test_get_functions(self):
        self.dajaxice._registry = []
        self.failUnlessEqual(self.dajaxice.get_functions(), [])
        
        self.dajaxice._registry = [DajaxiceModule('a.function','a.function'), DajaxiceModule('b.function','b.function')]
        self.failUnlessEqual(len(self.dajaxice.get_functions()), 2)
        
        self.failUnlessEqual(type(self.dajaxice.get_functions()[0]), DajaxiceModule)
        self.failUnlessEqual(type(self.dajaxice.get_functions()[1]), DajaxiceModule)
    
    def test_exist_module(self):
        self.dajaxice._registry = [DajaxiceModule('a.function','a.function'), DajaxiceModule('b.function','b.function')]
        self.failUnlessEqual(self.dajaxice._exist_module('a'), 0)
        self.failUnlessEqual(self.dajaxice._exist_module('b'), 1)
        self.assertFalse(self.dajaxice._exist_module('c'))
    
    def test_register(self):
        from ajax import test_foo, test_foo_with_params
        self.dajaxice.register(test_foo)
        self.dajaxice.register(test_foo_with_params)
        
        name = '%s.%s' % (test_foo.__module__, test_foo.__name__)
        name2 = '%s.%s' % (test_foo_with_params.__module__, test_foo_with_params.__name__)
        
        self.assertTrue(name in self.dajaxice._callable)
        self.assertTrue(name2 in self.dajaxice._callable)
        self.failUnlessEqual(len(self.dajaxice._callable), 2)
        
        self.failUnlessEqual(len(self.dajaxice._registry), 1)
        self.failUnlessEqual(type(self.dajaxice._registry[0]), DajaxiceModule)
        #further testing is needed
        