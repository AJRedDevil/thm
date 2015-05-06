# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PricingModel'
        db.create_table(u'pricing_pricingmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estimated_hours', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('complexity', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=100, decimal_places=2)),
        ))
        db.send_create_signal(u'pricing', ['PricingModel'])


    def backwards(self, orm):
        # Deleting model 'PricingModel'
        db.delete_table(u'pricing_pricingmodel')


    models = {
        u'pricing.complexityrate': {
            'Meta': {'object_name': 'ComplexityRate'},
            'complexity_rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '1000', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pricing.hourrate': {
            'Meta': {'object_name': 'HourRate'},
            'hour_rate': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pricing.pricingmodel': {
            'Meta': {'object_name': 'PricingModel'},
            'complexity': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '100', 'decimal_places': '2'}),
            'estimated_hours': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pricing']