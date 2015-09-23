

import logging
import simplejson as json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .handler import MetricManager
from thm.decorators import is_superuser

# Init Logger
logger = logging.getLogger(__name__)

# Create your views here.

mm = MetricManager()

@login_required
@is_superuser
def dashboard(request):
    """Dashboard to display the graphs
    """
    user = request.user
    return render(request, 'dashboard.html', locals())
    
@login_required
@is_superuser
def chardDataJSON(request):
    """Returns the json data for charts
    """
    data={}
    params=request.GET
    request_graph=params.get('name','')
    if request_graph == 'jobType':
        data=mm.get_job_type_info()
    elif request_graph == 'jobStatus':
        data=mm.get_jobs_status_info()
    elif request_graph == 'userJobsCount':
        data=mm.get_user_jobs_count()
    elif request_graph == 'revenue':
        data=mm.get_revenue()
    elif request_graph == 'jobTypePerYear':
        data=mm.get_job_type_per_year_info()
    elif request_graph == 'revenuePerYear':
        data=mm.get_revenue_per_year()

    return HttpResponse(json.dumps(data), content_type='application/json')
