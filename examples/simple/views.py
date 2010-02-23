from django.shortcuts import render_to_response
from django.conf import settings

def simple_index(request):
	return render_to_response('simple/simple_index.html')