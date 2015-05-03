# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'PricingModel.estimated_time'
        db.alter_column(u'pricing_pricingmodel', 'estimated_time', self.gf('django.db.models.fields.DecimalField')(max_digits=100, decimal_places=2))

    def backwards(self, orm):

        # Changing field 'PricingModel.estimated_time'
        db.alter_column(u'pricing_pricingmodel', 'estimated_time', self.gf('django.db.models.fields.IntegerField')(max_length=3))

    models = {
        u'pricing.complexityrate': {
            'Meta': {'object_name': 'ComplexityRate'},
            'complexity_rate': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pricing.hourrate': {
            'Meta': {'object_name': 'HourRate'},
            'hour_rate': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'pricing.pricingmodel': {
            'Meta': {'object_name': 'PricingModel'},
            'complexity': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '100', 'decimal_places': '2'}),
            'estimated_time': ('django.db.models.fields.DecimalField', [], {'default': '1.0', 'max_digits': '100', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_unit_selection': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        }
    }

    complete_apps = ['pricing']