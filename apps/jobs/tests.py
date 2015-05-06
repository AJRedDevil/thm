from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


from .models import Jobs
from apps.users.models import UserProfile
import logging
# Create your tests here.


class JobTestCase(TestCase):
    """
    Unit Test cases for Jobs Module
    """

    def setUp(self):
        super(JobTestCase, self).setUp()
        self.client = Client()
        self.staffphone = "+9779802036633"
        self.staffname = "admin"
        self.staffpassword1 = "test123"
        self.staffpassword2 = "test123"
        self.staffcity = "Kathmandu"
        self.staffstreetaddress = "Thirbum Marg - 4, Baluwatar"

        self.customerphone = "+9779847023944"
        self.customername = "customer"
        self.customerpassword1 = "test123"
        self.customerpassword2 = "test123"
        self.customercity = "Kathmandu"
        self.customerstreetaddress = "Bakhundole, Lalitpur"
        self.customerpost_data = dict(
            phone=self.customerphone,
            name=self.customername,
            password1=self.customerpassword1,
            password2=self.customerpassword2,
            city=self.customercity,
            streetaddress=self.customerstreetaddress,
        )

        # create user
        user = UserProfile(
            phone=self.staffphone,
            name=self.staffname,
            is_superuser=True,
            user_type=0,
            address=dict(
                streetaddress=self.staffstreetaddress,
                city=self.staffcity),
        )
        user.set_password(self.staffpassword1)
        user.save()

        # create customer
        self.customer = UserProfile(
            phone=self.customerphone,
            name=self.customername,
            is_superuser=True,
            user_type=2,
            address=dict(
                streetaddress=self.customerstreetaddress,
                city=self.customercity),
        )
        self.customer.set_password(self.customerpassword1)
        self.customer.save()

    def test1_createJobUrl(self):
        # Login to the system
        login_post_data = dict(
            phone=self.staffphone,
            password=self.staffpassword1
        )
        response = self.client.post(reverse('signin'), data=login_post_data)
        # Open Job Creation Page
        response = self.client.get(reverse('createJob'))
        self.assertEqual(response.status_code, 200)
        # Create job post data
        job_post_data = dict(
            customer=self.customer.id,
            jobtype='1',
            remarks='test plumbing job'
        )
        response = self.client.post(reverse('createJob'), data=job_post_data)
        self.assertEqual(response.status_code, 302)
        # Get the job reference id
        job = Jobs.objects.get(remarks='test plumbing job')
        # Open the job page
        response = self.client.get(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref})
        )
        self.assertEqual(response.status_code, 200)

    def test1_UpdateJobUrl(self):
        # Login to the system
        login_post_data = dict(
            phone=self.staffphone,
            password=self.staffpassword1
        )
        response = self.client.post(reverse('signin'), data=login_post_data)
        # Open Job Creation Page
        response = self.client.get(reverse('createJob'))
        self.assertEqual(response.status_code, 200)
        # Create job post data
        job_post_data = dict(
            customer=self.customer.id,
            jobtype='1',
            remarks='test plumbing job',
        )
        response = self.client.post(reverse('createJob'), data=job_post_data)
        self.assertEqual(response.status_code, 302)
        # Get the job reference id
        job = Jobs.objects.get(id=1)
        # Open the job page
        response = self.client.get(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref})
        )
        self.assertEqual(response.status_code, 200)
        # Update the job data
        job_update_data = dict(
            customer=self.customer.id,
            jobtype='1',
            remarks='test job',
            status='0',
            fee_0='0.00',
            fee_1='NPR'
        )
        response = self.client.post(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref}),
            data=job_update_data
        )
        self.assertEqual(response.status_code, 200)
        job = Jobs.objects.get(id=1)
        self.assertEqual(job.remarks, job_update_data['remarks'])
        # Open the job page
        response = self.client.get(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref})
        )
        self.assertEqual(response.status_code, 200)
        # Update job status
        # Change from New to Accepted
        job_update_data = dict(
            customer=self.customer.id,
            jobtype='1',
            remarks='test job',
            status='1',
            fee_0='0.00',
            fee_1='NPR'
        )
        response = self.client.post(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref}),
            data=job_update_data
        )
        self.assertEqual(response.status_code, 200)
        job = Jobs.objects.get(id=1)
        self.assertEqual(job.status, job_update_data['status'])
        # Open the job page
        response = self.client.get(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref})
        )
        self.assertEqual(response.status_code, 200)
        # Update job status back to New
        old_status = job.status
        job_update_data = dict(
            customer=self.customer.id,
            jobtype='1',
            remarks='test job',
            status='0',
            fee_0='0.00',
            fee_1='NPR'
        )
        response = self.client.post(
            reverse('viewJob',
                    kwargs={'job_id': job.jobref}),
            data=job_update_data
        )
        self.assertEqual(response.status_code, 200)
        job = Jobs.objects.get(id=1)
        self.assertNotEqual(job.status, job_update_data['status'])
        self.assertEqual(job.status, old_status)
