# -*- coding: utf-8 -*-
import pytz
import datetime
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone

def get_timezone_aware(_date): 
    tzinfo=pytz.timezone("Asia/Kathmandu")
    try:
        if _date.is_aware():
            return _date
    except AttributeError, err:
        try:
            if _date.tzinfo:
                return _date
        except AttributeError, err:
            return timezone.make_aware(_date, tzinfo)

def get_inspection_starting_datetime(start_date):
    return get_timezone_aware(datetime.datetime.combine(start_date, datetime.time(hour=10)))

def get_inspection_ending_date(start_date, hours):
    _end = start_date + datetime.timedelta(hours=hours)
    return get_timezone_aware(_end)

def get_accepted_ending_date(start_date, hours):
    _end = start_date + datetime.timedelta(hours=hours)
    return get_timezone_aware(_end)

def get_completion_starting_date(end_date, hours):
    _start = end_date - datetime.timedelta(hours=hours)
    return get_timezone_aware(_start)

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JobScheduler'
        db.create_table(u'jobs_jobscheduler', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.Jobs'])),
            ('inspection_start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('inspection_end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('job_start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('job_end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'jobs', ['JobScheduler'])

        # Create Job Scheduler for current jobs
        for obj in orm['jobs.Jobs'].objects.filter().order_by('id'):
            try:
                job_scheduler = orm.JobScheduler.objects.get(job=obj)
            except orm.JobScheduler.DoesNotExist, err:
                status = False if obj.status in ['0', '4', '5'] else True
                if obj.status == '1':
                    job_scheduler = orm.JobScheduler(
                    job=obj,
                    active=status,
                    inspection_start_date=get_inspection_starting_datetime(obj.inspection_date),
                    inspection_end_date=get_inspection_ending_date(get_inspection_starting_datetime(obj.inspection_date), 1)
                    )
                elif obj.status == '2':
                    job_scheduler = orm.JobScheduler(
                        job=obj,
                        active=status,
                        inspection_start_date=get_inspection_starting_datetime(obj.inspection_date),
                        inspection_end_date=get_inspection_ending_date(get_inspection_starting_datetime(obj.inspection_date), 1),
                        job_start_date=get_timezone_aware(obj.accepted_date),
                        job_end_date=get_accepted_ending_date(obj.accepted_date, 4)
                        )
                elif obj.status == '3':
                    job_scheduler = orm.JobScheduler(
                        job=obj,
                        active=status,
                        inspection_start_date=get_inspection_starting_datetime(obj.inspection_date),
                        inspection_end_date=get_inspection_ending_date(get_inspection_starting_datetime(obj.inspection_date), 1),
                        job_start_date=get_completion_starting_date(obj.completion_date, 4),
                        job_end_date=get_timezone_aware(obj.completion_date)
                        )
                else:
                    job_scheduler = orm.JobScheduler(
                    job=obj,
                    active=status
                    )
                job_scheduler.save()


    def backwards(self, orm):
        # Deleting model 'JobScheduler'
        db.delete_table(u'jobs_jobscheduler')


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
            'jobref': ('django.db.models.fields.CharField', [], {'default': "'9cd89410c19b417493ffba7aa390a31e'", 'unique': 'True', 'max_length': '100'}),
            'jobtype': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'location_landmark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'})
        },
        u'jobs.jobscheduler': {
            'Meta': {'object_name': 'JobScheduler'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'inspection_start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Jobs']"}),
            'job_end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'job_start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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
            'userref': ('django.db.models.fields.CharField', [], {'default': "'149b12765a434ee6856cf869c297c9e5'", 'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['jobs']