from django.core.mail import send_mail, EmailMessage
from django.conf import settings

class EmailSender:
    def __init__(self, subject: str, message: str, to_emails: list, from_email: str = None):
        self.subject = subject
        self.message = message
        self.to_emails = to_emails
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL

    def send_simple(self, fail_silently=False):
        return send_mail(
            subject=self.subject,
            message=self.message,
            from_email=self.from_email,
            recipient_list=self.to_emails,
            fail_silently=fail_silently
        )

    def send_html(self, html_content: str = None, fail_silently=False):
        email = EmailMessage(
            subject=self.subject,
            body=self.message,
            from_email=self.from_email,
            to=self.to_emails,
        )
        if html_content:
            email.content_subtype = 'html'
            email.body = html_content
        return email.send(fail_silently=fail_silently)
