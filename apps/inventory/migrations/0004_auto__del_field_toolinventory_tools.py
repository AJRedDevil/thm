# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ToolInventory.tools'
        db.delete_column(u'inventory_toolinventory', 'tools')

        # Adding M2M table for field tools on 'ToolInventory'
        m2m_table_name = db.shorten_name(u'inventory_toolinventory_tools')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('toolinventory', models.ForeignKey(orm[u'inventory.toolinventory'], null=False)),
            ('inventory', models.ForeignKey(orm[u'inventory.inventory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['toolinventory_id', 'inventory_id'])


    def backwards(self, orm):
        # Adding field 'ToolInventory.tools'
        db.add_column(u'inventory_toolinventory', 'tools',
                      self.gf('jsonfield.fields.JSONField')(default='{}', max_length=9999),
                      keep_default=False)

        # Removing M2M table for field tools on 'ToolInventory'
        db.delete_table(db.shorten_name(u'inventory_toolinventory_tools'))


    models = {
        u'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        u'inventory.toolinventory': {
            'Meta': {'object_name': 'ToolInventory'},
            'handyman': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'toolHolder'", 'to': u"orm['users.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tools': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'handset'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['inventory.Inventory']"})
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
            'userref': ('django.db.models.fields.CharField', [], {'default': "'524418e388dd4fd6bc6ec08b78b93302'", 'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['inventory']