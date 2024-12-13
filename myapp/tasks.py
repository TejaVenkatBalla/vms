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

from django.utils.timezone import now
from .models import PurchaseOrder
from datetime import timedelta


@shared_task
def send_delivery_deadline_reminders():
    """
    Sends reminders to vendors for Purchase Orders with upcoming delivery deadlines.
    """
    # Get the current date and calculate the upcoming deadline (e.g., 3 days ahead)
    #print("in sch")
    current_date = now()
    deadline_threshold = current_date + timedelta(days=3)

    # Find Purchase Orders with upcoming deadlines
    upcoming_deadlines = PurchaseOrder.objects.filter(
        delivery_date__lte=deadline_threshold,  # Deadline is within 3 days
        delivery_date__gte=current_date,       # Deadline is not in the past
        status='pending'                       # Ensure only pending orders are notified
    )

    for po in upcoming_deadlines:
        # Send an email to the vendor
        vendor_email = po.vendor.email  # Assuming email is in contact_details
        if vendor_email:
            send_mail(
                subject=f"Reminder: Delivery Deadline Approaching for PO {po.po_number}",
                message=f"Dear {po.vendor.name},\n\n"
                        f"This is a reminder that the delivery deadline for Purchase Order {po.po_number} "
                        f"is approaching on {po.delivery_date.strftime('%Y-%m-%d %H:%M:%S')}.\n\n"
                        f"Please ensure timely delivery to avoid any delays.\n\n"
                        f"Best regards,\nYour Vendor Management Team",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[vendor_email],
            )
