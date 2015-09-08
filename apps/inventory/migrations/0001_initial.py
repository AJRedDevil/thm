# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Inventory'
        db.create_table(u'inventory_inventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('purchased_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
            ('price_currency', self.gf('djmoney.models.fields.CurrencyField')(default='NPR')),
            ('price', self.gf('djmoney.models.fields.MoneyField')(max_digits=8, decimal_places=2, default_currency='NPR')),
            ('purchased_from', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_damaged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('damaged_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_lost', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lost_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=1024, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Inventory'])


    def backwards(self, orm):
        # Deleting model 'Inventory'
        db.delete_table(u'inventory_inventory')


    models = {
        u'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'damaged_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'is_damaged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_lost': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lost_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'price': ('djmoney.models.fields.MoneyField', [], {'max_digits': '8', 'decimal_places': '2', 'default_currency': "'NPR'"}),
            'price_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'NPR'"}),
            'purchased_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'purchased_from': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['inventory']