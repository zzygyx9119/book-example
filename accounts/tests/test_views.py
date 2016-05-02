from unittest.mock import call, patch

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core import mail

from accounts.models import Token

class LoginViewTest(TestCase):
    url = reverse('login')

    def test_get_login_url_renders_login_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'login.html')


    def test_post_email_creates_token(self):
        email = 'elspeth@example.com'
        response = self.client.post(self.url, data=dict(email=email))
        token = Token.objects.get(email=email)
        self.assertEqual(len(token.uid), 36)


    def test_post_email_redirects_to_login_page(self):
        email = 'elspeth@example.com'
        response = self.client.post(self.url, data=dict(email=email))
        self.assertRedirects(response, self.url)


    @patch('accounts.views.send_mail')
    def test_post_email_sends_email(self, mock_send_mail):
        email = 'elspeth@example.com'
        response = self.client.post(self.url, data=dict(email=email))
        self.assertEqual(mock_send_mail.called, True)
        (subject, body, frm, to_list), _ = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login code for superlists')
        token = Token.objects.get(email=email)
        self.assertIn('Use this code to log in:', body)
        self.assertIn(token.uid, body)
        self.assertEqual(frm, 'noreply@superlists')
        self.assertEqual(to_list, [email])


