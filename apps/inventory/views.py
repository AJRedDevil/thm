

import json
import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import InventoryCreationForm, InventoryEditFromAdmin, ToolDistributionForm, ToolDistributionFromAdmin
from .handler import InventoryManager
from thm.decorators import is_superuser

logger = logging.getLogger(__name__)

# Create your views here.

@login_required
@is_superuser
def createInventory(request):
    """View to create inventory"""
    user = request.user
    im = InventoryManager()
    if request.method == "GET":
        inventory_form = InventoryCreationForm()
        return render(request, 'createinventory.html', locals())
    elif request.method == "POST":
        inventory_form = InventoryCreationForm(request.POST, request.FILES)
        if inventory_form.is_valid():
            inventory_form.save()
            inventories = im.getAllInvetories()
            return render(request, 'inventorylist.html', locals())
        if inventory_form.errors:
            logging.warn("Form has errors, %s", inventory_form.errors)
        return render(request, 'createinventory.html', locals())

@login_required
@is_superuser
def viewInventory(request, inventory_id=None):
    """View to show the invetories
    """
    user = request.user
    im = InventoryManager()
    inventory_edit=False
    if request.method == "POST" and user.is_superuser:
        inventory = im.getInventoryDetails(inventory_id)
        inventory_form = InventoryEditFromAdmin(request.POST, request.FILES, instance=inventory)
        if inventory_form.is_valid():
            inventory_form.save()
            inventories = im.getAllInvetories()
            return render(request, 'inventorylist.html', locals())
    elif inventory_id is not None and user.is_superuser:
        inventory = im.getInventoryDetails(inventory_id)
        inventory_form = InventoryEditFromAdmin(instance=inventory)
        inventory_edit=True
        return render(request, 'viewinventory.html', locals())
    else:
        inventories = im.getAllInvetories()

    return render(request, 'inventorylist.html', locals())

@login_required
@is_superuser
def distributeTool(request, tool_id=None):
    """View to show the Tool Distribution
    """
    user = request.user
    im = InventoryManager()
    distribution_edit = False
    if request.method == "POST" and user.is_superuser:
        tool_distribution_form = ToolDistributionForm(request.POST)
        if tool_distribution_form.is_valid():
            tool_distribution = tool_distribution_form.save(commit=False)
            tool_distribution.save()
            tools_selected = request.POST.getlist("tools")
            for tool_id in tools_selected:
                inventory = im.getInventoryDetails(inventory_id=tool_id)
                tool_distribution.tools.add(inventory)
            # tool_distribution.save()
            tool_distribution_form.save_m2m()
            tools = im.getAllTools()
            return render(request, 'distributionlist.html', locals())
        if tool_distribution_form.errors:
            logging.warn("Form has errors, %s", tool_distribution_form.errors)
    else:
        tool_distribution_form = ToolDistributionForm()
    return render(request, 'toolsdistribution.html', locals())

@login_required
@is_superuser
def viewToolDistribution(request, tool_id=None):
    """View to show the tools distributed
    """
    user = request.user
    im = InventoryManager()
    tools_edit=False
    if request.method == "POST" and user.is_superuser:
        tool = im.getToolDetails(tool_id)
        tool_distribution_form = ToolDistributionFromAdmin(request.POST, instance=tool)
        if tool_distribution_form.is_valid():
            tool_distribution = tool_distribution_form.save(commit=False)
            tool_distribution.save()
            tools_selected = request.POST.getlist("tools")
            for tool_id in tools_selected:
                inventory = im.getInventoryDetails(inventory_id=tool_id)
                tool_distribution.tools.add(inventory)
            tool_distribution_form.save_m2m()
            tools = im.getAllTools()
            render(request, 'distributionlist.html', locals())
    elif tool_id is not None and user.is_superuser:
        tool = im.getToolDetails(tool_id)
        tool_distribution_form = ToolDistributionFromAdmin(instance=tool)
        tools = im.getAllTools(tool_handyman=tool)
        tool_distributed=True
        return render(request, 'viewToolDistribution.html', locals())
    else:
        tools = im.getAllTools()
    return render(request, 'distributionlist.html', locals())


