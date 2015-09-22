

from django.conf.urls import patterns, include, url


from apps.metrics import views as metricsView

urlpatterns = patterns('',
    url(r'^$', metricsView.dashboard, name="dashboard"),
    url(r'chartDataJson/$', metricsView.chardDataJSON, name="chart_data_json"),
)
