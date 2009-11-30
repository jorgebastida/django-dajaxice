from django.utils import simplejson

def test_string(request):
    return simplejson.dumps({'string':'hello world'})

def test_ajax_exception(request):
    raise Exception()
    return
    
def test_foo(request):
    return ""
    
def test_foo_with_params(request):
    return simplejson.dumps(dict(request.POST))