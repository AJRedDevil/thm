# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ComplexityRate'
        db.create_table(u'pricing_complexityrate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('complexity_rate', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=1000, decimal_places=2)),
        ))
        db.send_create_signal(u'pricing', ['ComplexityRate'])

        # Adding model 'HourRate'
        db.create_table(u'pricing_hourrate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hour_rate', self.gf('jsonfield.fields.JSONField')(default='{}', max_length=9999)),
        ))
        db.send_create_signal(u'pricing', ['HourRate'])


    def backwards(self, orm):
        # Deleting model 'ComplexityRate'
        db.delete_table(u'pricing_complexityrate')

        # Deleting model 'HourRate'
        db.delete_table(u'pricing_hourrate')


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
        }
    }

    complete_apps = ['pricing']