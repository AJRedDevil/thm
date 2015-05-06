from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


from phonenumber_field.modelfields import PhoneNumber
# Create your tests here.
from apps.users.models import UserProfile, EarlyBirdUser
import users.handler as user_handler
from apps.users.forms import EBUserPhoneNumberForm

import logging

class UserTestCase(TestCase):
    """
    Tests signup case
    """
    def setUp(self):
        super(UserTestCase, self).setUp()
        self.client = Client()
        self.phone = "9802036633"
        self.name = "test"
        self.password1 = "test123"
        self.password2 = "test123"
        self.city   = "Kathmandu"
        self.streetaddress = "Sukedhara, Baluwatar"
        self.post_data = dict(
            phone=self.phone,
            name=self.name,
            password1=self.password1,
            password2=self.password2,
            city=self.city,
            streetaddress=self.streetaddress,
            )

    def test1_SignupUrl(self):
        response = self.client.get('/signup/')
        self.assertNotEqual(response.status_code, 200)

    def test2_UserIsCreated(self):
        response = self.client.post('/signup/', data=self.post_data)
        user = None
        try:
            user = UserProfile.objects.get(phone=self.phone)
        except Exception, e:
            self.assertEqual(user, None)
        self.assertNotEqual(response.status_code, 302)
        # self.assertEqual(user.phone, PhoneNumber.from_string(self.phone))
        # self.assertEqual(user.address['streetaddress'], self.streetaddress)

    def test3_LogoutUrl(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test4_SigninUrl(self):
        response = self.client.get(reverse('signin'))
        # signin page is disabled for now
        self.assertEqual(response.status_code, 302)

    def test5_Signin(self):
        post_data=dict(
            phone=self.phone,
            password=self.password1
            )
        response = self.client.post('/signup/', data=self.post_data)
        response = self.client.get(reverse('logout'))
        response = self.client.post(reverse('signin'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, 'http://testserver/home/')

    def test6_RedirectHomeIfSignedin(self):
        post_data=dict(
            phone=self.phone,
            password=self.password1
            )
        self.client.post('/signup/', data=self.post_data)
        response = self.client.post(reverse('signin'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, 'http://testserver/home/')
        # do not open the signup page for logged in users
        response = self.client.get('/signup/')
        self.assertNotEqual(response.status_code, 302)

    def test7_MyProfilePage(self):
        post_data = dict(
            phone=self.phone,
            password=self.password1
        )
        self.client.post('/signup/', data=self.post_data)
        response = self.client.post(reverse('signin'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, 'http://testserver/home/')
        response = self.client.get('/profile/')
        self.assertNotEqual(response.status_code, 200)

    def test8_MySettingsPage(self):
        new_city = 'Bhaktapur'
        new_streetaddress = 'Gatthaghar'
        post_data = dict(
            phone=self.phone,
            password=self.password1
        )
        self.client.post('/signup/', data=self.post_data)
        response = self.client.post(reverse('signin'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'http://testserver/home/')
        response = self.client.get(reverse('userSettings'))
        self.assertEqual(response.status_code, 200)
        post_data = dict(
            phone=self.phone,
            name=self.name,
            city=new_city,
            streetaddress=new_streetaddress
        )
        response = self.client.post(reverse('userSettings'), data=post_data)
        self.assertEqual(response.status_code, 302)
        um = user_handler.UserManager()
        userdetails = um.getUserDetails('1')
        self.assertEqual(userdetails.address['city'], new_city)
        # Update with invalid phone
        new_phone = "0944-7023944"
        post_data = dict(
            phone=new_phone,
            name=self.name,
            city=new_city,
            streetaddress=new_streetaddress
        )
        response = self.client.post(reverse('userSettings'), data=post_data)
        self.assertNotEqual(response.status_code, 302)
        um = user_handler.UserManager()
        userdetails = um.getUserDetails('1')
        self.assertNotEqual(userdetails.phone.as_national, new_phone)
        # Update with valid phone
        new_phone = "0984-7023945"
        post_data = dict(
            phone=new_phone,
            name=self.name,
            city=new_city,
            streetaddress=new_streetaddress
        )
        response = self.client.post(reverse('userSettings'), data=post_data)
        self.assertEqual(response.status_code, 302)
        um = user_handler.UserManager()
        userdetails = um.getUserDetails('1')
        self.assertEqual(userdetails.phone.as_national, new_phone)


class PhoneNumberTestCase(TestCase):
    """
    Phone test case
    """
    def setUp(self):
        super(PhoneNumberTestCase, self).setUp()
        self.phone_regular_valid = ["+9779802036633","9802036633", "9779802036633"]
        self.phone_land_line = ["+97714412832", "+14412832", "4412832", "97714412832", "9774412832"]
        self.phone_non_nep = ["+8801732987388", "+16627368514"]
        self.phone_ncell = ["9801036633", "9803197607"]
        self.phone_ntc_mobile = ["9841136633", "9841891459"]
        self.phone_utl_mobile = ["9721122112"]
        self.phone_ndcl_mobile = ["9741122112", "9741122112"]
        self.phone_nstpl_mobile = ["9631122112"]
        self.phone_stm_mobile = ["9601122112"]
        self.phone_smartcell_mobile=["9611122112"]

    def test1_validRegularPhone(self):
        ## Tests Valid phone
        for x in self.phone_regular_valid:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)


    def test2_invalidPhoneLandLine(self):
        ## Tests regular landline
        for x in self.phone_land_line:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertNotEqual(user_form.is_valid(), True)

    def test3_invalidNonNepalesePhone(self):
        ## Tests invalid mobile for non nepalese phone
        for x in self.phone_non_nep:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertNotEqual(user_form.is_valid(), True)

    def test4_validPhoneNcell(self):
        ## Tests valid Ncell mobile
        for x in self.phone_ncell:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

    def test5_validPhoneNtc(self):
        ### Tests valid NTC mobile
        for x in self.phone_ntc_mobile:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

    def test6_validPhoneUTL(self):
        ### Tests valid UTL
        for x in self.phone_utl_mobile:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

    def test7_validPhoneNDCLMobile(self):
        for x in self.phone_ndcl_mobile:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

    def test8_validPhoneNSTPLMobile(self):
        for x in self.phone_nstpl_mobile:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

    def test9_validPhoneSTMMobile(self):
        for x in self.phone_stm_mobile:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

    def test10_validPhoneSmartCellMobile(self):
        for x in self.phone_smartcell_mobile:
            post_data = dict(
                phone=x,
                )
            user_form = EBUserPhoneNumberForm(data=post_data)
            self.assertEqual(user_form.is_valid(), True)

class EBUserTestCase(TestCase):
    """
    Tests for Early Bird Users
    """
    def setUp(self):
        super(EBUserTestCase, self).setUp()
        self.client = Client()
        self.phone = "+977 984-7023944"
        self.to = "2200"
        self.text = "Handyman"
        self.timestamp = "2015-01-09 10%3A00%3A12"
        self.get_data = dict(
            # from=self.phone,
            to=self.to,
            text=self.text,
            timestamp=self.timestamp,
            )

    def test1_register_from_homepage(self):
        post_data=dict(
            phone=self.phone
            )
        self.client.post(reverse('register'), data=post_data)
        ebuser = EarlyBirdUser.objects.get(id=1)
        self.assertEqual(ebuser.phone.as_international, self.phone)

