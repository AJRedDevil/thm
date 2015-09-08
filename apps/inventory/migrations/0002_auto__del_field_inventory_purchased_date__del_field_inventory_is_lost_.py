# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Inventory.purchased_date'
        db.delete_column(u'inventory_inventory', 'purchased_date')

        # Deleting field 'Inventory.is_lost'
        db.delete_column(u'inventory_inventory', 'is_lost')

        # Deleting field 'Inventory.is_damaged'
        db.delete_column(u'inventory_inventory', 'is_damaged')

        # Deleting field 'Inventory.lost_date'
        db.delete_column(u'inventory_inventory', 'lost_date')

        # Deleting field 'Inventory.damaged_date'
        db.delete_column(u'inventory_inventory', 'damaged_date')

        # Deleting field 'Inventory.price_currency'
        db.delete_column(u'inventory_inventory', 'price_currency')

        # Deleting field 'Inventory.purchased_from'
        db.delete_column(u'inventory_inventory', 'purchased_from')

        # Deleting field 'Inventory.price'
        db.delete_column(u'inventory_inventory', 'price')


    def backwards(self, orm):
        # Adding field 'Inventory.purchased_date'
        db.add_column(u'inventory_inventory', 'purchased_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Inventory.is_lost'
        db.add_column(u'inventory_inventory', 'is_lost',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Inventory.is_damaged'
        db.add_column(u'inventory_inventory', 'is_damaged',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Inventory.lost_date'
        db.add_column(u'inventory_inventory', 'lost_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Inventory.damaged_date'
        db.add_column(u'inventory_inventory', 'damaged_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Inventory.price_currency'
        db.add_column(u'inventory_inventory', 'price_currency',
                      self.gf('djmoney.models.fields.CurrencyField')(default='NPR'),
                      keep_default=False)

        # Adding field 'Inventory.purchased_from'
        db.add_column(u'inventory_inventory', 'purchased_from',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2015, 6, 29, 0, 0), max_length=100),
                      keep_default=False)

        # Adding field 'Inventory.price'
        db.add_column(u'inventory_inventory', 'price',
                      self.gf('djmoney.models.fields.MoneyField')(max_digits=8, decimal_places=2, default_currency='NPR'),
                      keep_default=False)


    models = {
        u'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['inventory']