# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FAQ'
        db.create_table(u'faq_faq', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('faqref', self.gf('django.db.models.fields.CharField')(default='ad7f261333cc41f3a62035bb8b4e1252', unique=True, max_length=100)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('answer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'faq', ['FAQ'])


    def backwards(self, orm):
        # Deleting model 'FAQ'
        db.delete_table(u'faq_faq')


    models = {
        u'faq.faq': {
            'Meta': {'object_name': 'FAQ'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'faqref': ('django.db.models.fields.CharField', [], {'default': "'624ffcdab4b04d26bfbd70c0a918c3fe'", 'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['faq']