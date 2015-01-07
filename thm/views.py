from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from thm.decorators import is_superuser
def index(request):
    """
    Returns Index Page
    """
    return render(request, 'index.html', locals())

@login_required
@is_superuser
def manage(request):
    """
    Returns mgmt links portal
    """
    user = request.user
    return render(request, 'admin.html', locals())
