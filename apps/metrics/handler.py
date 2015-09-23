
import datetime
import logging
from django.db.models import Sum
from django.utils import timezone

from apps.commcalc.models import Commission
from apps.jobs.models import Jobs
from apps.users.models import UserProfile

JOB_TYPE=['N/A','Plumbing','Electrical','Furnishing','Construction']

class MetricManager(object):

    def __init__(self):
        self.start_year, self.end_year = self.__get_start_end_date()


    def __convert_naive_to_aware(self, _date):
        return datetime.datetime.combine(_date,datetime.time(0,0))

    def __get_start_end_date(self,):
        current_date=timezone.now().date()
        current_year=current_date.year
        start_year=self.__convert_naive_to_aware(datetime.datetime(current_year,1,1))
        end_year=self.__convert_naive_to_aware(datetime.datetime(current_year,12,31))
        return (start_year, end_year)

    def get_jobs_status_info(self, start_date=None, end_date=None):
        """Returns the total jobs status count for start_date and end_date
        """
        status=['New','Inspection','Accepted','Completed','Rejected','Discarded']
        status_count=[0]*len(status)
        if start_date and end_date:
            pass
        else:
            jobs=Jobs.objects.all()
            total=float(len(jobs))
            for job in jobs:
                index=int(job.status)
                status_count[index] += 1
        return [dict(name=status[i],y=round(status_count[i]/total*100,2)) for i in range(len(status))]

    def get_job_type_info(self, start_date=None, end_date=None):
        """Returns the total jobs type count for start_date and end_date
        """
        type_count=[0]*len(JOB_TYPE)
        if start_date and end_date:
            pass
        else:
            jobs=Jobs.objects.all()
            for job in jobs:
                index=int(job.jobtype)
                type_count[index] += 1
        return [dict(name=JOB_TYPE[i],data=[type_count[i]]) for i in range(len(JOB_TYPE))]

    def get_user_jobs_count(self,):
        """Return the total jobs and users per month
        """
        # start_year, end_year = self.__get_start_end_date()
        jobs=Jobs.objects.filter(creation_date__range=[self.start_year, self.end_year])
        users=UserProfile.objects.filter(date_joined__range=[self.start_year, self.end_year] ,user_type=2)
        jobs_count=[0]*12
        users_count=[0]*12
        for job in jobs:
            jobs_count[job.creation_date.month - 1] += 1
        for user in users:
            users_count[user.date_joined.month - 1] += 1
        data=[{'name':'Jobs', 'data':jobs_count},{'name':'Users','data':users_count}]
        return data

    def get_revenue(self,):
        """Return the revenue stream
        """
        jobs = Jobs.objects.filter(status=3)
        commissions = Commission.objects.filter(is_paid=True).aggregate(Sum('amount'))
        data=[]
        # users
        data.append(UserProfile.objects.filter(user_type=2, is_active=True).count())
        # handymen
        data.append(UserProfile.objects.filter(user_type=1, is_active=True).count())
        revenue=jobs.aggregate(Sum('fee'))['fee__sum']
        data.append("Rs.{:,.2f}".format(revenue))
        # revenue per user
        data.append("Rs.{:,.2f}".format(round(revenue/jobs.values('customer').distinct().count(), 2)))
        # revenue per job
        data.append("Rs.{:,.2f}".format(round(revenue/jobs.count(),2)))
        data.append("Rs.{:,.2f}".format(commissions['amount__sum']))
        return data

    def get_job_type_per_year_info(self):
        """Return job type per year
        """
        jobs=Jobs.objects.filter(creation_date__range=[self.start_year, self.end_year])
        job_type_count={str(i):[0]*12 for i in range(len(JOB_TYPE))}
        for job in jobs:
            job_type_count[job.jobtype][job.creation_date.month - 1] += 1
        return [dict(name=JOB_TYPE[i],data=job_type_count[str(i)]) for i in range(len(JOB_TYPE))]

    def get_revenue_per_year(self):
        """Return revenue per year
        """
        REVENUE_STREAM = ['Total Revenue'] + JOB_TYPE[1:]
        revenue={str(i):[0]*12 for i in range(len(REVENUE_STREAM))}
        jobs=Jobs.objects.filter(creation_date__range=[self.start_year, self.end_year], status=3)
        for job in jobs:
            revenue['0'][job.completion_date.month - 1] += job.fee.amount
            revenue[job.jobtype][job.completion_date.month - 1] += job.fee.amount
        return [dict(name=REVENUE_STREAM[int(i)],data=revenue[i]) for i in sorted(revenue.keys())]

        