from django.shortcuts import render


def simple_index(request):
    return render(request, 'simple/simple_index.html')
