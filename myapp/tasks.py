from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_vendor_notification_email(email, subject, message):
    """
    Task to send an email notification to the vendor asynchronously.
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )