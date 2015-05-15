# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Commission.handyman'
        db.add_column(u'commcalc_commission', 'handyman',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='handyman', to=orm['users.UserProfile']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Commission.handyman'
        db.delete_column(u'commcalc_commission', 'handyman_id')


    models = {
        u'commcalc.commission': {
            'Meta': {'object_name': 'Commission'},
            'amount': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'NPR'", 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'amount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'NPR'"}),
            'handyman': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'handyman'", 'to': u"orm['users.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobs': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commission'", 'to': u"orm['jobs.Jobs']"})
        },
        u'jobs.jobs': {
            'Meta': {'object_name': 'Jobs'},
            'accepted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'comm_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs'", 'to': u"orm['users.UserProfile']"}),
            'fee': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'NPR'", 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'fee_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'NPR'"}),
            'handyman': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orders'", 'symmetrical': 'False', 'to': u"orm['users.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ishidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jobref': ('django.db.models.fields.CharField', [], {'default': "'b294dabfde754f7faccd92007fc87330'", 'unique': 'True', 'max_length': '100'}),
            'jobtype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_landmark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1'}),
            'address': ('jsonfield.fields.JSONField', [], {'default': "{'city': 'Kathmandu', 'streetaddress': 'Tripureshwore'}", 'max_length': '9999', 'blank': 'True'}),
            'address_coordinates': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'current_address': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('phonenumber_field.modelfields.PhoneNumberField', [], {'unique': 'True', 'max_length': '16'}),
            'phone_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'userref': ('django.db.models.fields.CharField', [], {'default': "'b563a30f44284df59d02b1ce55920856'", 'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['commcalc']