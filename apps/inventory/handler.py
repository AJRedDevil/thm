

import logging


from django.core import serializers
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Inventory, ToolInventory

logger = logging.getLogger(__name__)

class InventoryManager(object):
    """Manager to handle inventory model
    """
    def getInventoryDetails(self, inventory_id):
        """List Inventory information
        """
        inventory = get_object_or_404(Inventory, id=inventory_id)
        return inventory

    def getAllInvetories(self, user=None):
        """List all the inventories
        """
        if user == None or user.user_type == 0:
            inventories = Inventory.objects.filter()
        elif user.user_type == 1:
            allInventories = Inventory.objects.exclude(handyman=None)
            inventories = [x for x in allInventories if user in x.handyman.all()]
        else:
            inventories = []

        logger.debug("Inventory Details: \n {0}".format(
            serializers.serialize('json', inventories))
        )
        return inventories

    def getAllInventoriesByDate(self, user, date):
        """Return list of inventories by date
        """
        if user.user_type == 0:
            inventories = Inventory.objects.filter(purchased_date__gte=date)
        elif user.user_type == 1:
            allInventories = Inventory.objects.filter(purchased_date__gte=date).exclude(handyman=None)
            inventories = [x for x in allInventories if user in x.handyman.all()]
        else:
            inventories = []

        logger.debug("Inventory Details: \n {0}".format(
            serializers.serialize('json', inventories))
        )
        return inventories

    def getAllTools(self, tool_handyman=None):
        """List all the tools for each handyman
        """
        handyman = None
        if tool_handyman is not None:
            handyman = tool_handyman.handyman
        if handyman == None:
            tools = ToolInventory.objects.all()
        else:
            tools = ToolInventory.objects.filter(handyman=handyman)

        logger.debug("Tools Details: \n {0}".format(
            serializers.serialize('json', tools))
        )
        return tools

    def getToolDetails(self, tool_id):
        """List Tool Distribution
        """
        tool = get_object_or_404(ToolInventory, id=tool_id)
        return tool

