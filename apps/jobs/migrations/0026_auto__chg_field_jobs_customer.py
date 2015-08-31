# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Jobs.customer'
        db.alter_column(u'jobs_jobs', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['subscription.Subscriber']))

        for obj in orm.Jobs.objects.all():
            customer=obj.customer
            subscriber=orm['Subscription.Subscriber'].objects.get(primary_contact_person=customer)
            obj.customer=subscriber
            obj.save()

    def backwards(self, orm):

        # Changing field 'Jobs.customer'
        db.alter_column(u'jobs_jobs', 'customer_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.UserProfile']))

    models = {
        u'jobs.jobevents': {
            'Meta': {'object_name': 'JobEvents'},
            'event': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Jobs']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'jobs.jobs': {
            'Meta': {'object_name': 'Jobs'},
            'accepted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'jobs_subscriber'", 'to': u"orm['subscription.Subscriber']"}),
            'fee': ('djmoney.models.fields.MoneyField', [], {'default_currency': "'NPR'", 'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'fee_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'NPR'"}),
            'handyman': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'orders'", 'symmetrical': 'False', 'to': u"orm['users.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'is_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ishidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jobref': ('django.db.models.fields.CharField', [], {'default': "'e69cb3366a8741fbaedc2367bb4422b4'", 'unique': 'True', 'max_length': '100'}),
            'jobtype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_landmark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'subscription.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_office': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'office_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '7'}),
            'primary_contact_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primaryContactPerson'", 'to': u"orm['users.UserProfile']"}),
            'secondary_contact_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secondaryContactPerson'", 'to': u"orm['users.UserProfile']"}),
            'subscriber_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
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
            'userref': ('django.db.models.fields.CharField', [], {'default': "'ccea4cba98a943258b38326e0bd40692'", 'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['jobs']