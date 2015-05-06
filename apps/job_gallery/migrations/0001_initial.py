# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JobGalleryImages'
        db.create_table(u'job_gallery_jobgalleryimages', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=1024, blank=True)),
            ('img_type', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2)),
        ))
        db.send_create_signal(u'job_gallery', ['JobGalleryImages'])


    def backwards(self, orm):
        # Deleting model 'JobGalleryImages'
        db.delete_table(u'job_gallery_jobgalleryimages')


    models = {
        u'job_gallery.jobgalleryimages': {
            'Meta': {'object_name': 'JobGalleryImages'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'img_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'})
        }
    }

    complete_apps = ['job_gallery']