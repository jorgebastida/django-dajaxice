from django.utils import simplejson

def example1(request):
    return simplejson.dumps({'message':'hello world'})
    
def example2(request):
    raise Exception("prueba")
    return simplejson.dumps({'numbers':[1,2,3]})

def example3(request, data, name):
    result = sum(map(int,data))
    return simplejson.dumps({'result':result})