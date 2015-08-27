# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubscriptionPackage'
        db.create_table(u'subscription_subscriptionpackage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=100)),
            ('price_currency', self.gf('djmoney.models.fields.CurrencyField')(default='NPR')),
            ('price', self.gf('djmoney.models.fields.MoneyField')(max_digits=8, decimal_places=2, default_currency='NPR')),
            ('max_repair', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3)),
            ('discount', self.gf('django.db.models.fields.DecimalField')(default=0.0, max_digits=100, decimal_places=2)),
        ))
        db.send_create_signal(u'subscription', ['SubscriptionPackage'])

        # Adding model 'Subscriber'
        db.create_table(u'subscription_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('primary_contact_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primaryContactPerson', to=orm['users.UserProfile'])),
            ('secondary_contact_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='secondaryContactPerson', to=orm['users.UserProfile'])),
            ('subscriber_name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('office_number', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=7)),
            ('is_office', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'subscription', ['Subscriber'])

        # Adding model 'Subscription'
        db.create_table(u'subscription_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(related_name='packageSelected', to=orm['subscription.SubscriptionPackage'])),
            ('terminated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('terminated_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriber', to=orm['subscription.Subscriber'])),
            ('repairs_completed', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal(u'subscription', ['Subscription'])

        # Create subscriber from current customers
        for obj in orm['users.UserProfile'].objects.filter(user_type=2):
            subscriber=orm.Subscriber(
                subscriber_name=obj.name,
                primary_contact_person=obj,
                secondary_contact_person=obj
                )
            subscriber.save()


    def backwards(self, orm):
        # Deleting model 'SubscriptionPackage'
        db.delete_table(u'subscription_subscriptionpackage')

        # Deleting model 'Subscriber'
        db.delete_table(u'subscription_subscriber')

        # Deleting model 'Subscription'
        db.delete_table(u'subscription_subscription')


    models = {
        u'subscription.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_office': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'office_number': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '7'}),
            'primary_contact_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primaryContactPerson'", 'to': u"orm['users.UserProfile']"}),
            'secondary_contact_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'secondaryContactPerson'", 'to': u"orm['users.UserProfile']"}),
            'subscriber_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        u'subscription.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'end_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'packageSelected'", 'to': u"orm['subscription.SubscriptionPackage']"}),
            'repairs_completed': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriber'", 'to': u"orm['subscription.Subscriber']"}),
            'terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'terminated_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'subscription.subscriptionpackage': {
            'Meta': {'object_name': 'SubscriptionPackage'},
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '100', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_repair': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '100'}),
            'price': ('djmoney.models.fields.MoneyField', [], {'max_digits': '8', 'decimal_places': '2', 'default_currency': "'NPR'"}),
            'price_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'NPR'"})
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
            'userref': ('django.db.models.fields.CharField', [], {'default': "'0d9cabb49ebb43edb3cc6f1ade8c3046'", 'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['subscription']