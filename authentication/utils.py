from django.core.mail import send_mail
from django.utils.html import strip_tags


def email_template(subject, mail_to, html_message):
    email_subject = subject
    html_format = html_message
    message = strip_tags(html_message)
    email_from = 'cinchstreamingservice@gmail.com'
    email_to = [mail_to]

    send_mail(email_subject, message, email_from, email_to, fail_silently=False, html_message=html_format)
