from django.core.management.base import BaseCommand
from dajaxice.core import DajaxiceRequest
from django.template.loader import render_to_string
from optparse import make_option

class Command(BaseCommand):
    help = "Generate dajaxice.core.js file to import it as static file"
    args = "[--compile]"
    option_list = BaseCommand.option_list + (
        make_option('--compile', default='no', dest='compile', help='Compile output using Google closure-compiler'),
    )
    
    requires_model_validation = False
    
    def handle(self, *app_labels, **options):
        compile_output = options.get('compile','yes')
        data = {'dajaxice_js_functions':DajaxiceRequest.get_js_functions(), 'DAJAXICE_URL_PREFIX': DajaxiceRequest.get_media_prefix()}
        js = render_to_string('dajaxice/dajaxice.core.js', data )
        if compile_output.lower() == "closure":
            print self.complie_js_with_closure(js)
        else:
            print js
        
    def complie_js_with_closure(self,js):
        import httplib, urllib, sys
        params = urllib.urlencode([
            ('js_code',js),
            ('compilation_level', 'ADVANCED_OPTIMIZATIONS'),
            ('output_format', 'text'),
            ('output_info', 'compiled_code'),
        ])
        # Always use the following value for the Content-type header.
        headers = { "Content-type": "application/x-www-form-urlencoded" }
        conn = httplib.HTTPConnection('closure-compiler.appspot.com')
        conn.request('POST', '/compile', params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return data