from django.shortcuts import render

def index(request):
    """
    Returns Index Page
    """
    return render(request, 'index.html', locals())