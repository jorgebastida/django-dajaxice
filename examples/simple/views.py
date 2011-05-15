from django.shortcuts import render_to_response


def simple_index(request):
    return render_to_response('simple/simple_index.html')
