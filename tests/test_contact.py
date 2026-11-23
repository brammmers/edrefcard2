"""The /contact form: SMTP sending, anti-spam guards and header safety."""
import os
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Blueprint, Flask

import contact
from extensions import limiter

TEMPLATES = Path(__file__).resolve().parents[1] / 'www' / 'templates'
SMTP_ENV = {
    'SMTP_HOST': 'smtp.example.test',
    'SMTP_PORT': '587',
    'SMTP_USER': 'mailbox@example.test',
    'SMTP_PASSWORD': 'test-password-not-a-real-secret',
    'CONTACT_TO': 'mailbox@example.test',
}
ORIGIN = {'Origin': 'http://localhost'}


def make_app():
    """The contact blueprint plus stubs of the 'web' endpoints base.html links to."""
    app = Flask(__name__, template_folder=str(TEMPLATES))
    app.secret_key = 'test-secret-not-a-real-secret'
    app.config['RATELIMIT_STORAGE_URI'] = 'memory://'
    web = Blueprint('web', __name__)
    for rule, name in (('/', 'index'), ('/privacy', 'privacy'), ('/ed.css', 'serve_css')):
        web.add_url_rule(rule, name, lambda: '')
    app.register_blueprint(web)
    app.register_blueprint(contact.contact_bp)
    app.context_processor(lambda: {'version': 'test'})
    limiter.init_app(app)
    return app


class ContactTests(unittest.TestCase):
    def setUp(self):
        env = patch.dict(os.environ, SMTP_ENV)
        env.start()
        self.addCleanup(env.stop)
        self.app = make_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            limiter.reset()
        smtp = patch('contact.smtplib.SMTP')
        self.smtp = smtp.start()
        self.addCleanup(smtp.stop)
        self.server = self.smtp.return_value

    def token(self, age=60):
        """A form token issued `age` seconds ago."""
        with self.app.app_context(), patch('itsdangerous.timed.time.time',
                                           return_value=time.time() - age):
            return contact.form_token()

    def post(self, headers=ORIGIN, age=60, **fields):
        data = {'subject': 'controller', 'card': 'custom-4-2-s8j5', 'email': 'cmdr@example.org',
                'message': 'My VKB Gladiator is not supported yet.', 'token': self.token(age)}
        data.update(fields)
        return self.client.post('/contact', data=data, headers=headers)

    def sent(self):
        self.assertEqual(self.server.send_message.call_count, 1)
        return self.server.send_message.call_args.args[0]

    # Page and configuration

    def test_get_prefills_subject_and_card(self):
        page = self.client.get('/contact?subject=controller&card=custom-4-2-s8j5').get_data(as_text=True)
        self.assertIn('value="custom-4-2-s8j5"', page)
        self.assertIn('<option value="controller" selected>', page)
        self.assertIn('name="website"', page)  # honeypot present

    def test_get_drops_invalid_prefill(self):
        page = self.client.get('/contact?subject=x&card=%3Cscript%3E').get_data(as_text=True)
        self.assertNotIn('<script>', page)
        self.assertNotIn('option value="x"', page)

    def test_missing_configuration_points_to_forum(self):
        os.environ.pop('SMTP_PASSWORD')
        page = self.client.get('/contact')
        self.assertEqual(page.status_code, 200)
        self.assertIn('unavailable', page.get_data(as_text=True))
        self.assertIn(contact.FORUM_URL, page.get_data(as_text=True))
        response = self.post()
        self.assertEqual(response.status_code, 503)
        self.smtp.assert_not_called()

    # Sending

    def test_valid_message_is_sent_from_the_mailbox(self):
        response = self.post()
        self.assertEqual(response.status_code, 302)
        self.assertIn('sent=1', response.headers['Location'])
        self.smtp.assert_called_once_with('smtp.example.test', 587, timeout=contact.SMTP_TIMEOUT)
        self.server.starttls.assert_called_once()
        self.server.login.assert_called_once_with('mailbox@example.test', SMTP_ENV['SMTP_PASSWORD'])
        msg = self.sent()
        self.assertIn('<mailbox@example.test>', msg['From'])
        self.assertEqual(msg['To'], 'mailbox@example.test')
        self.assertEqual(msg['Reply-To'], 'cmdr@example.org')
        self.assertEqual(msg['Subject'], '[EDRefCard] Missing controller (custom-4-2-s8j5)')
        body = msg.get_content()
        self.assertIn('https://edrefcard.info/binds/custom-4-2-s8j5', body)
        self.assertIn('IP: 127.0.0.1', body)
        self.assertIn('User-Agent:', body)
        self.assertIn('My VKB Gladiator', body)
        self.assertIn('Message sent', self.client.get(response.headers['Location']).get_data(as_text=True))

    def test_without_email_there_is_no_reply_to(self):
        self.post(email='', card='')
        msg = self.sent()
        self.assertIsNone(msg['Reply-To'])
        self.assertEqual(msg['Subject'], '[EDRefCard] Missing controller')
        self.assertNotIn('/binds/', msg.get_content())

    def test_pasted_card_link_is_reduced_to_its_reference(self):
        self.post(card='https://edrefcard.info/binds/custom-4-2-s8j5?x=1')
        self.assertIn('(custom-4-2-s8j5)', self.sent()['Subject'])

    def test_smtp_failure_keeps_the_message_and_hides_details(self):
        self.server.login.side_effect = OSError('535 bad credentials for mailbox@example.test')
        response = self.post()
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 502)
        self.assertIn('could not be sent', page)
        self.assertIn('My VKB Gladiator', page)
        self.assertNotIn('535', page)

    def test_port_465_uses_implicit_tls(self):
        os.environ['SMTP_PORT'] = '465'
        with patch('contact.smtplib.SMTP_SSL') as smtp_ssl:
            self.post()
        server = smtp_ssl.return_value
        server.send_message.assert_called_once()
        server.starttls.assert_not_called()
        self.smtp.assert_not_called()

    # Anti-spam

    def test_honeypot_fakes_success_without_sending(self):
        response = self.post(website='http://spam.example')
        self.assertEqual(response.status_code, 302)
        self.assertIn('sent=1', response.headers['Location'])
        self.smtp.assert_not_called()

    def test_too_fast_submit_is_rejected(self):
        response = self.post(age=0)
        self.assertEqual(response.status_code, 400)
        self.assertIn('very quick', response.get_data(as_text=True))
        self.smtp.assert_not_called()

    def test_forged_or_stale_token_is_rejected(self):
        for token in ('forged', self.token(age=contact.MAX_FORM_AGE + 60)):
            response = self.post(token=token)
            self.assertEqual(response.status_code, 400)
            self.assertIn('expired', response.get_data(as_text=True))
        self.smtp.assert_not_called()

    def test_cross_origin_post_is_blocked(self):
        self.assertEqual(self.post(headers={'Origin': 'https://evil.example'}).status_code, 403)
        self.assertEqual(self.post(headers={}).status_code, 403)
        self.smtp.assert_not_called()

    def test_rate_limit_after_five_posts(self):
        for _ in range(5):
            self.assertEqual(self.post().status_code, 302)
        self.assertEqual(self.post().status_code, 429)
        self.assertEqual(self.server.send_message.call_count, 5)
        self.assertEqual(self.client.get('/contact').status_code, 200)  # GET stays open

    # Validation and header injection

    def test_header_injection_in_email_is_rejected(self):
        for email in ('cmdr@example.org\r\nBcc: victim@example.org',
                      'cmdr@example.org\nSubject: spam',
                      'Someone <cmdr@example.org>',
                      'a@b.c, other@example.org'):
            response = self.post(email=email)
            self.assertEqual(response.status_code, 400, email)
            self.assertIn('does not look valid', response.get_data(as_text=True))
        self.smtp.assert_not_called()

    def test_subject_outside_the_list_is_rejected(self):
        for subject in ('other\r\nBcc: victim@example.org', 'Free money', ''):
            self.assertEqual(self.post(subject=subject).status_code, 400, subject)
        self.smtp.assert_not_called()

    def test_card_reference_with_header_characters_is_rejected(self):
        for card in ('abc\r\nBcc: victim@example.org', '../etc/passwd', '<b>x</b>'):
            self.assertEqual(self.post(card=card).status_code, 400, card)
        self.smtp.assert_not_called()

    def test_error_is_shown_under_the_faulty_field(self):
        response = self.post(card='Que passes-t-il', message='Mon contrôleur disparait !')
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn('id="card-error"', page)
        self.assertIn('class="invalid" aria-invalid="true" aria-describedby="card-error" autofocus', page)
        self.assertIn('One field needs a correction', page)
        self.assertNotIn('id="message-error"', page)
        self.assertIn('value="Que passes-t-il"', page)  # what was typed is kept
        self.assertIn('Mon contrôleur disparait !', page)
        self.smtp.assert_not_called()

    def test_several_faulty_fields_focus_the_first_one(self):
        page = self.post(card='a b', email='nope', message='').get_data(as_text=True)
        self.assertIn('Some fields need a correction', page)
        for name in ('card', 'email', 'message'):
            self.assertIn(f'id="{name}-error"', page)
        self.assertEqual(page.count(' autofocus'), 1)
        self.assertIn('aria-describedby="card-error" autofocus', page)

    def test_message_length_limits(self):
        self.assertEqual(self.post(message='hi').status_code, 400)
        response = self.post(message='x' * (contact.MESSAGE_MAX + 1))
        self.assertEqual(response.status_code, 400)
        self.assertIn('too long', response.get_data(as_text=True))
        self.smtp.assert_not_called()

    def test_message_body_newlines_stay_in_the_body(self):
        self.post(message='Line one\r\nBcc: victim@example.org\r\n\r\nLine three')
        msg = self.sent()
        self.assertIsNone(msg['Bcc'])
        self.assertIn('Bcc: victim@example.org', msg.get_content())


if __name__ == '__main__':
    unittest.main()
