from django.core.mail import send_mail
from django.utils.html import strip_tags
from random import randint


def email_template(subject, mail_to, html_message):
    email_subject = subject
    html_format = html_message
    message = strip_tags(html_message)
    email_from = 'cinchstreamingservice@gmail.com'
    email_to = [mail_to]

    send_mail(email_subject, message, email_from, email_to, fail_silently=False, html_message=html_format)


def generate_otp():
    range_start = 10 ** (6 - 1)
    range_end = (10 ** 6) - 1
    otp = randint(range_start, range_end)
    otp = str(otp)
    return otp
