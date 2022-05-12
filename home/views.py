from django.shortcuts import render

# Create your views here.


def index(request):
    '''Render landing page'''
    return render(request, 'home/index.html')
