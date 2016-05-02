import os
import poplib
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

from django.test import override_settings
from django.core import mail

from .base import FunctionalTest

TEST_EMAIL = 'edith.testuser@yahoo.com'
CODE_FINDER = r'^Use this code to log in: (.+)$'


class LoginTest(FunctionalTest):

    def wait_for_email(self, subject):
        subject_line = 'Subject: {}'.format(subject)
        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(TEST_EMAIL)
            inbox.pass_(os.environ.get('YAHOO_PASSWORD'))
            while time.time() - start < 60:
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    if subject_line in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()


    def wait_for_page_to_contain(self, expected_text):
        body_locator = (By.TAG_NAME, "body")
        WebDriverWait(self.browser, 10).until(
            expected_conditions.text_to_be_present_in_element(
                body_locator, expected_text
            )
        )


    @override_settings(EMAIL_BACKEND=mail._original_email_backend)
    def test_login_via_email(self):
        # Edith goes to the awesome superlists site
        # and notices a "Sign in" link for the first time.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A new page appears with the option to enter her email
        self.browser.find_element_by_css_selector(
            'input[type="email"]'
        ).send_keys(TEST_EMAIL + '\n')

        # The page refreshes and says "email sent"
        self.wait_for_page_to_contain(
            "Email sent to edith.testuser@yahoo.com",
        )

        # Shortly, she receives an email with a code in
        email_text = self.wait_for_email('Your login code for superlists')
        result = re.search(CODE_FINDER, email_text, re.MULTILINE)
        if not result:
            self.fail('could not find {} in {}'.format(CODE_FINDER, email_text))
        code = result.group(1)
        print(code)

        # She types the code in
        self.browser.find_element_by_css_selector(
            'input[name="uid"]'
        ).send_keys(code + '\n')

        # She can see that she is logged in
        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.ID, 'id_logout'))
        )
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('edith.testuser@yahoo.com', navbar.text)

