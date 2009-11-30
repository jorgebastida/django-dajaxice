from django.utils import simplejson

def example1(request):
    return simplejson.dumps({'message':'hello world'})
    
def example2(request):
    return simplejson.dumps({'numbers':[1,2,3]})