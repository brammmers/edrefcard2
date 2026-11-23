"""Contact form: /contact sends one plain-text mail to the maintainers' mailbox.

Configuration comes from the environment (docker-compose.prod.yml forwards it):
SMTP_HOST, SMTP_PORT (587 = STARTTLS, 465 = implicit TLS), SMTP_USER,
SMTP_PASSWORD and CONTACT_TO. Without them the page says the form is
unavailable and points to the forum thread instead of failing.

The mail is sent FROM the mailbox itself (SPF and DMARC pass); the visitor's
address, when given, only goes in Reply-To.

Anti-spam without captcha: a hidden honeypot field, a signed timestamp that
rejects forms sent too quickly, a same-origin check, and a per-IP rate limit.
"""
import os
import re
import smtplib
import ssl
import time
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from urllib.parse import urlparse

from flask import (Blueprint, abort, current_app, redirect, render_template,
                   request, url_for)
from flask_limiter.util import get_remote_address
from itsdangerous import BadSignature, URLSafeTimedSerializer

from extensions import limiter

contact_bp = Blueprint('contact', __name__)

FORUM_URL = 'https://forums.frontier.co.uk/threads/627609/'
CARD_URL = 'https://edrefcard.info/binds/{}'

SUBJECTS = {
    'controller': 'Missing controller',
    'card': 'Wrong card',
    'other': 'Other',
}
MESSAGE_MAX = 5000
MESSAGE_MIN = 10
EMAIL_MAX = 254
CARD_MAX = 100
# A human needs a few seconds to read the page and type a message; a form
# older than a day is stale (and its token could have been harvested).
MIN_FILL_SECONDS = 3
MAX_FORM_AGE = 24 * 3600
SMTP_TIMEOUT = 15
HONEYPOT_FIELD = 'website'

# Deliberately strict: one address, no spaces, no CR/LF, no quotes or angle
# brackets, so the Reply-To header cannot carry anything else.
_EMAIL_RE = re.compile(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+")
_CARD_RE = re.compile(r'[A-Za-z0-9_-]{1,%d}' % CARD_MAX)  # same rule as Config.isValidName


def smtp_settings():
    """The SMTP settings, or None when the form is not configured."""
    settings = {
        'host': os.environ.get('SMTP_HOST', '').strip(),
        'port': os.environ.get('SMTP_PORT', '').strip() or '587',
        'user': os.environ.get('SMTP_USER', '').strip(),
        'password': os.environ.get('SMTP_PASSWORD', ''),
        'to': os.environ.get('CONTACT_TO', '').strip(),
    }
    if not all((settings['host'], settings['user'], settings['password'], settings['to'])):
        return None
    try:
        settings['port'] = int(settings['port'])
    except ValueError:
        return None
    return settings


def _serializer():
    return URLSafeTimedSerializer(current_app.secret_key, salt='contact-form')


def form_token():
    """Signed token holding the time the form was served."""
    return _serializer().dumps('contact')


def form_age(token):
    """Seconds since the token was issued, or None when it is invalid or stale."""
    try:
        _, issued = _serializer().loads(token or '', max_age=MAX_FORM_AGE, return_timestamp=True)
    except BadSignature:  # also covers SignatureExpired
        return None
    return time.time() - issued.timestamp()


def valid_email(value):
    return (isinstance(value, str) and len(value) <= EMAIL_MAX
            and _EMAIL_RE.fullmatch(value) is not None)


def valid_card(value):
    return isinstance(value, str) and _CARD_RE.fullmatch(value) is not None


def same_origin():
    """Same rule as the admin CSRF guard: Origin (or Referer) must be this host."""
    for header in ('Origin', 'Referer'):
        value = request.headers.get(header)
        if value:
            return urlparse(value).netloc == request.host
    return False


def validate(form):
    """Return (clean values, error messages)."""
    values = {
        'email': (form.get('email') or '').strip(),
        'subject': form.get('subject') or '',
        'card': (form.get('card') or '').strip(),
        'message': (form.get('message') or '').replace('\r\n', '\n').strip(),
    }
    errors = []
    if values['email'] and not valid_email(values['email']):
        errors.append('This email address does not look valid. Leave it empty if you do not want a reply.')
    if values['subject'] not in SUBJECTS:
        errors.append('Please choose what your message is about.')
    if values['card']:
        # Accept a pasted card link as well as the bare reference.
        match = re.search(r'/binds/([^/?#\s]+)', values['card'])
        if match:
            values['card'] = match.group(1)
        if not valid_card(values['card']):
            errors.append('The card reference may only contain letters, digits, "-" and "_" '
                          '(for example custom-4-2-s8j5).')
    if len(values['message']) < MESSAGE_MIN:
        errors.append('Please write a message (a few words at least).')
    elif len(values['message']) > MESSAGE_MAX:
        errors.append(f'Your message is too long ({len(values["message"])} characters, '
                      f'{MESSAGE_MAX} at most).')
    return values, errors


def build_message(values, settings, ip, user_agent):
    """The mail to the maintainers. Only validated values reach the headers."""
    msg = EmailMessage()
    subject = f'[EDRefCard] {SUBJECTS[values["subject"]]}'
    if values['card']:
        subject += f' ({values["card"]})'
    msg['Subject'] = subject
    msg['From'] = formataddr(('EDRefCard contact form', settings['user']))
    msg['To'] = settings['to']
    msg['Message-ID'] = make_msgid(domain=settings['user'].rpartition('@')[2] or None)
    if values['email']:
        msg['Reply-To'] = values['email']

    lines = [
        f'Subject: {SUBJECTS[values["subject"]]}',
        f'Reply to: {values["email"] or "(no address given)"}',
    ]
    if values['card']:
        lines.append(f'Card: {CARD_URL.format(values["card"])}')
    lines += [
        f'IP: {ip}',
        f'User-Agent: {user_agent[:300]}',
        '',
        values['message'],
        '',
    ]
    msg.set_content('\n'.join(lines))
    return msg


def send_message(msg, settings):
    """Send through the mailbox's SMTP server (STARTTLS on 587, TLS on 465)."""
    context = ssl.create_default_context()
    if settings['port'] == 465:
        server = smtplib.SMTP_SSL(settings['host'], settings['port'],
                                  timeout=SMTP_TIMEOUT, context=context)
    else:
        server = smtplib.SMTP(settings['host'], settings['port'], timeout=SMTP_TIMEOUT)
    with server:
        if settings['port'] != 465:
            server.starttls(context=context)
        server.login(settings['user'], settings['password'])
        server.send_message(msg)


def _log(text):
    try:
        from scripts import logError
        logError(text)
    except Exception:
        print(text, end='')


@contact_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit('5 per hour', methods=['POST'])
def contact_form():
    settings = smtp_settings()
    context = {'subjects': SUBJECTS, 'forum_url': FORUM_URL, 'available': settings is not None,
               'message_max': MESSAGE_MAX, 'honeypot': HONEYPOT_FIELD}

    if request.method == 'GET':
        subject = request.args.get('subject', '')
        card = request.args.get('card', '')
        values = {'email': '', 'message': '',
                  'subject': subject if subject in SUBJECTS else '',
                  'card': card if valid_card(card) else ''}
        return render_template('contact.html', values=values, errors=[],
                               sent=request.args.get('sent') == '1',
                               token=form_token(), **context)

    if not same_origin():
        abort(403, description='Cross-origin request blocked')
    values, errors = validate(request.form)
    if settings is None:
        return render_template('contact.html', values=values, errors=[], sent=False,
                               token=form_token(), **context), 503

    # Bots that fill every field get a fake success and no mail.
    if request.form.get(HONEYPOT_FIELD):
        _log(f'contact: honeypot filled by {get_remote_address()}\n')
        return redirect(url_for('contact.contact_form', sent=1))

    age = form_age(request.form.get('token'))
    if age is None:
        errors.insert(0, 'This form has expired. Please send it again.')
    elif age < MIN_FILL_SECONDS:
        errors.insert(0, 'That was very quick. Please check your message and send it again.')

    if errors:
        return render_template('contact.html', values=values, errors=errors, sent=False,
                               token=form_token(), **context), 400

    msg = build_message(values, settings, get_remote_address(),
                        request.headers.get('User-Agent', ''))
    try:
        send_message(msg, settings)
    except Exception as e:  # never echo the server's reply: it may quote credentials
        _log(f'contact: cannot send mail ({type(e).__name__})\n')
        errors = ['Your message could not be sent right now. Please try again later, '
                  'or post it on the forum thread.']
        return render_template('contact.html', values=values, errors=errors, sent=False,
                               token=form_token(), **context), 502
    return redirect(url_for('contact.contact_form', sent=1))
