from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


from .models import Jobs
from users.models import UserProfile
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
        self.staffcity   = "Kathmandu"
        self.staffstreetaddress = "Thirbum Marg - 4, Baluwatar"

        self.customerphone = "+9779847023944"
        self.customername = "customer"
        self.customerpassword1 = "test123"
        self.customerpassword2 = "test123"
        self.customercity   = "Kathmandu"
        self.customerstreetaddress = "Bakhundole, Lalitpur"
        self.customerpost_data = dict(
            phone=self.customerphone,
            name=self.customername,
            password1=self.customerpassword1,
            password2=self.customerpassword2,
            city=self.customercity,
            streetaddress=self.customerstreetaddress,
            )

    def test1_createJobUrl(self):
        # create user
        user = UserProfile(
            phone=self.staffphone,
            name=self.staffname,
            is_superuser=True,
            user_type=0,
            address=dict(streetaddress=self.staffstreetaddress,city=self.staffcity),
            )
        user.set_password(self.staffpassword1)
        user.save()
        # create customer
        customer = UserProfile(
            phone=self.customerphone,
            name=self.customername,
            is_superuser=True,
            user_type=2,
            address=dict(streetaddress=self.customerstreetaddress,city=self.customercity),
            )
        customer.set_password(self.customerpassword1)
        customer.save()
        # Login to the system
        login_post_data=dict(
            phone=self.staffphone,
            password=self.staffpassword1
            )
        response = self.client.post(reverse('signin'), data=login_post_data)
        # Open Job Creation Page
        response = self.client.get(reverse('createJob'))
        self.assertEqual(response.status_code, 200)
        # Create job post data
        job_post_data=dict(
            customer=customer.id,
            jobtype = '1',
            remarks = 'test plumbing job'
            )
        response = self.client.post(reverse('createJob'), data=job_post_data)
        self.assertEqual(response.status_code, 200)
        # Get the job reference id
        job = Jobs.objects.get(id=1)
        # Open the job page
        response = self.client.get(reverse('viewJob', kwargs={'job_id': job.jobref}))
        self.assertEqual(response.status_code, 200)
