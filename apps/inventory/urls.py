from django.conf.urls import patterns, url

from apps.inventory import views as inventoryView

urlpatterns = patterns(
    '',
    url(r'^viewinventory/(?P<inventory_id>[\w\d]+)/$', inventoryView.viewInventory, name='viewInventory'),
    url(r'^$', inventoryView.viewInventory, name="inventory"),
    url(r'^createinventory/$', inventoryView.createInventory, name='createInventory'),
    url(r'^distributetool/$', inventoryView.distributeTool, name="distributeTool"),
    url(r'^viewtooldistribution/(?P<tool_id>[\w\d]+)/$', inventoryView.viewToolDistribution, name='viewToolDistribution'),
    url(r'^viewtooldistributionlist/$', inventoryView.viewToolDistribution, name='viewDistributionList'),
)
