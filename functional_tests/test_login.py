import re
from django.core import mail

from .base import FunctionalTest

class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section in the navbar for the first time
        # It's telling her to enter her email address, so she does

        self.browser.get(self.server_url)
        self.browser.find_element_by_name('email').send_keys('edith@mailinator.com\n')

        # A message appears telling her an email has been sent
        alert = self.browser.find_element_by_css_selector('li.alert-success')
        self.assertIn('Check your email', alert.text)

        # She checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn('edith@mailinator.com', email.to)
        self.assertEqual(email.subject, 'Your login link for Superlists')


        # It has a url link in it
        self.assertIn('Use this link to log in', email.body)
        email_finder = re.search(r'http://.+/.+/', email.body)
        self.assertIsNotNone(email_finder)
        url = email_finder.group(0)
        self.assertIn(self.server_url, url)

        # she clicks it
        self.browser.get(url)

        # she is logged in!
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('edith@mailinator.com', navbar.text)


