from django.test import TestCase
from tangra.views import *
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY


# Example: 
# https://github.com/django/django-old/blob/master/django/contrib/auth/tests/views.py


class HomeMethodTests(TestCase):
	
	def test_home_with_no_logged_in_user(self):
		"""	This should redirect to the login page """
		client = Client()
		response = client.get(reverse('home'))
		self.assertRedirects(
			response, 
			reverse('login'), 
			status_code=302, 
			target_status_code=200, 
		)

	def test_home_with_logged_in_user(self):
		""" This should redirect to the studies page """
		client = Client()
		User.objects.create_user('test', 'test@tangra.com', 'asdf')
		self.assertTrue(client.login(username='test', password='asdf'))
		response = client.get(reverse('home'))
		self.assertRedirects(
			response, 
			reverse('studies:active_studies'), 
			status_code=302, 
			target_status_code=200,
		)


class LoginMethodTests(TestCase):

	def confirm_logged_in(self, client):
		self.assert_(SESSION_KEY in client.session)
	
	def test_view_login_page_while_not_logged_in(self):
		"""	Test viewing the login page while not already logged in """
		client = Client()
		response = client.get(reverse('login'))
		self.assertEqual(response.status_code, 200)

	def test_view_login_page_while_logged_in(self):
		"""	Test viewing the login page while already logged in. Should redirect 
		the user back to home. """
		client = Client()
		User.objects.create_user('test', 'test@tangra.com', 'asdf')
		self.assertTrue(client.login(username='test', password='asdf'))
		self.confirm_logged_in(client)
		response = client.get(reverse('login'))
		self.assertRedirects(
			response, 
			reverse('home'), 
			status_code=302, 
			target_status_code=302,
		)

	def test_login_with_success(self):
		""" Logging in successfully should redirect back to the home page """
		client = Client()
		User.objects.create_user('test', 'test@tangra.com', 'asdf')
		response = client.post(reverse('login'), {'username':'test', 'password':'asdf'})
		self.assertEqual(response.status_code, 302)
		self.confirm_logged_in(client)

	def test_login_with_disabled_account(self):
		""" Logging in with an account that has been disabled """
		client = Client()
		user = User.objects.create_user('test', 'test@tangra.com', 'asdf')
		user.is_active = False
		user.save()
		response = client.post(reverse('login'), {'username':'test', 'password':'asdf'})
		self.assertEqual(response.status_code, 200)
		self.assert_(response.context['errors'])
		self.assertEqual(response.context['message'], ERROR_DISABLED_ACCOUNT)

	def test_login_with_invalid_username(self):
		"""	Logging in with an incorrect username or password """
		client = Client()
		user = User.objects.create_user('test', 'test@tangra.com', 'asdf')
		response = client.post(reverse('login'), {'username':'tester', 'password':'asdf'})
		self.assertEqual(response.status_code, 200)
		self.assert_(response.context['errors'])
		self.assertEqual(response.context['message'], ERROR_INVALID_CREDENTIALS)

	def test_login_with_invalid_password(self):
		client = Client()
		user = User.objects.create_user('test', 'test@tangra.com', 'asdf')
		response = client.post(reverse('login'), {'username':'test', 'password':'1234'})
		self.assertEqual(response.status_code, 200)
		self.assert_(response.context['errors'])
		self.assertEqual(response.context['message'], ERROR_INVALID_CREDENTIALS)

	def test_login_with_bad_request(self):
		"""	This is a result of not doing either a GET or POST.
		Should return a 405 HttpResponseNotAllowed status code. """
		pass


class LogoutMethodTests(TestCase):

	def login(self, client, username='test', password='asdf'):
		User.objects.create_user(username, 'test@tangra.com', password)
		self.assertTrue(client.login(username=username, password=password))
		self.assert_(SESSION_KEY in client.session)

	def confirm_logged_out(self, client):
		self.assert_(SESSION_KEY not in client.session)

	def test_logout_with_signed_in_user(self):
		"""	Test logging out of Tangra when there is a user already logged in """
		client = Client()
		self.login(client)
		response = client.get(reverse('logout'))
		self.assertRedirects(
			response, 
			reverse('home'), 
			status_code=302, 
			target_status_code=302, 
		)
		self.confirm_logged_out(client)
	
	def test_logout_with_no_signed_in_user(self):
		"""	Test logging out of Tangra when there is no user logged in already """
		client = Client()
		response = client.get(reverse('logout'))
		self.assertRedirects(
			response, 
			reverse('home'), 
			status_code=302, 
			target_status_code=302, 
		)
		self.confirm_logged_out(client)