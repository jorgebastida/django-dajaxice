#----------------------------------------------------------------------
# Copyright (c) 2010 Benito Jorge Bastida
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
from django.test import TestCase
from django.conf import settings

from dajaxice.exceptions import FunctionNotCallableError
from dajaxice.core import DajaxiceRequest
from dajaxice.core.DajaxiceRequest import DAJAX_MODERN_IMPORT

class DjangoIntegrationTest(TestCase):
    
    urls = 'dajaxice.tests.urls'
    
    def setUp(self):
        settings.DAJAXICE_MEDIA_PREFIX = "dajaxice"
        settings.DAJAXICE_DEBUG = False
        os.environ['DJANGO_SETTINGS_MODULE'] = 'dajaxice'
        
    def test_calling_not_registered_function(self):
        settings.DAJAXICE_FUNCTIONS = ()
        
        self.failUnlessRaises(FunctionNotCallableError,self.client.post, '/dajaxice/tests.test_string/',{'callback':'my_callback'})

    def test_calling_registered_function(self):
        settings.DAJAXICE_FUNCTIONS = ('tests.ajax.test_foo',)
        
        response = self.client.post('/dajaxice/tests.test_foo/',{'callback':'my_callback'})
        
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content,'my_callback()')

    def test_calling_registered_function_with_params(self):
        settings.DAJAXICE_FUNCTIONS = ('tests.ajax.test_foo_with_params',)
        
        response = self.client.post('/dajaxice/tests.test_foo_with_params/',{'callback':'my_callback', 'param1': 'value1'})
        
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content,'my_callback({"callback": ["my_callback"], "param1": ["value1"]})')
        
    def test_bad_function(self):
        settings.DAJAXICE_FUNCTIONS = ('tests.ajax.test_ajax_exception',)
        
        response = self.client.post('/dajaxice/tests.test_ajax_exception/',{'callback':'my_callback'})
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.content,"my_callback('DAJAXICE_EXCEPTION')")
    
    def test_is_callable(self):
        settings.DAJAXICE_FUNCTIONS = ('tests.ajax.test_ajax_registered',)
        
        dr = DajaxiceRequest(None, 'tests.test_ajax_registered')
        self.failUnless(dr._is_callable())
        
        dr = DajaxiceRequest(None, 'tests.test_ajax_not_registered')
        self.failIf(dr._is_callable())
        
    def test_get_js_functions(self):
        settings.DAJAXICE_FUNCTIONS = ('test1.ajax.a',
                                       'test2.ajax.b',
                                       'test2.ajax.c',
                                       'test3.ajax.d',)
                                       
        js_functions = DajaxiceRequest.get_js_functions()
        
        self.failUnlessEqual(len(js_functions), 3)
        self.failUnless('test1' in js_functions.keys())
        self.failUnless('test2' in js_functions.keys())
        self.failUnless('test3' in js_functions.keys())
        
        self.failUnlessEqual(len(js_functions.get('test1')), 1)
        self.failUnless('a' in js_functions.get('test1'))
        
        self.failUnlessEqual(len(js_functions.get('test2')), 2)
        self.failUnless('b' in js_functions.get('test2'))
        self.failUnless('c' in js_functions.get('test2'))
        
        self.failUnlessEqual(len(js_functions.get('test3')), 1)
        self.failUnless('d' in js_functions.get('test3'))

    def test_get_ajax_function(self):
        settings.DAJAXICE_FUNCTIONS = ('tests.ajax.test_foo',)
        
        # Test modern Import with a real ajax function
        dr = DajaxiceRequest(None, 'tests.test_foo')
        function = dr._modern_get_ajax_function()
        self.failUnless(hasattr(function, '__call__') )
        
        # Test old Import with a real ajax function
        dr = DajaxiceRequest(None, 'tests.test_foo')
        function = dr._old_get_ajax_function()
        self.failUnless(hasattr(function, '__call__') )
        
        # Test modern Import without a real ajax function
        dr = DajaxiceRequest(None, 'tests.test_foo2')
        self.failUnlessRaises(ImportError, dr._modern_get_ajax_function)
        
        # Test old Import without a real ajax function
        dr = DajaxiceRequest(None, 'tests.test_foo2')
        self.failUnlessRaises(ImportError, dr._old_get_ajax_function)
        