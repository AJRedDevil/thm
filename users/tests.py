from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


from phonenumber_field.modelfields import PhoneNumber
# Create your tests here.
from users.models import UserProfile

class UserTestCase(TestCase):
    """
    Tests signup case
    """
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.client = Client()
        self.phone = "+9779802036633"
        self.name = "test"
        self.password1 = "test123"
        self.password2 = "test123"
        self.city   = "Kathmandu"
        self.streetaddress = "Thirbum Marg - 4, Baluwatar"
        self.post_data = dict(
            phone=self.phone,
            name=self.name,
            password1=self.password1,
            password2=self.password2,
            city=self.city,
            streetaddress=self.streetaddress,
            )

    def test1_SignupUrl(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test2_UserIsCreated(self):
        response = self.client.post(reverse('signup'), data=self.post_data)
        user = UserProfile.objects.get(phone=self.phone)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.phone, PhoneNumber.from_string(self.phone))

    def test3_LogoutUrl(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test4_SigninUrl(self):
        response = self.client.get(reverse('signin'))
        self.assertEqual(response.status_code, 200)

    def test5_Signin(self):
        post_data=dict(
            phone=self.phone,
            password=self.password1
            )
        response = self.client.post(reverse('signup'), data=self.post_data)
        response = self.client.get(reverse('logout'))
        response = self.client.post(reverse('signin'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/home/')

    def test6_RedirectHomeIfSignedin(self):
        post_data=dict(
            phone=self.phone,
            password=self.password1
            )
        self.client.post(reverse('signup'), data=self.post_data)
        response = self.client.post(reverse('signin'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/home/')
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        
