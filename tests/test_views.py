from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class LoginViewTest(TestCase):

	def test_view_url_exists_at_desired_location(self):
		resp = self.client.get('/login/')
		self.assertEqual(resp.status_code, 200)

	def test_view_url_accessible_by_name(self):
		resp = self.client.get(reverse('login'))
		self.assertEqual(resp.status_code, 200)

	def test_view_uses_correct_template(self):
		resp = self.client.get(reverse('login'))
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'litresapp/login.html')


class LogoutViewTest(TestCase):

	def test_view_url_exists_at_desired_location(self):
		resp = self.client.get('/logout/')
		self.assertEqual(resp.status_code, 302)

	def test_view_url_accessible_by_name(self):
		resp = self.client.get(reverse('logout'))
		self.assertEqual(resp.status_code, 302)

	def test_view_uses_correct_redirect(self):
		resp = self.client.get(reverse('logout'))
		self.assertEqual(resp.status_code, 302)
		self.assertRedirects(resp, '/login/')


class BookListViewTest(TestCase):

	def test_view_url_exists_at_desired_location(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 302)

	def test_view_url_accessible_by_name(self):
		resp = self.client.get(reverse('book_list'))
		self.assertEqual(resp.status_code, 302)

	def test_view_uses_correct_redirect(self):
		resp = self.client.get(reverse('book_list'))
		self.assertEqual(resp.status_code, 302)
		self.assertRedirects(resp, '/login/')
