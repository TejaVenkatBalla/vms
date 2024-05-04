from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Avg, F


class Vendor(models.Model):
    # below 4 are mandatory to be displayed
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)

    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    '''
    Using the `delivery_date` for both the expected and actual delivery date of the order might seem fine initially.
    However, while performing calculations for `on_time_delivery_rate` there will be cases where the delivered date 
    exceeds the current time (late delivery). In such cases, the `on_time_delivery_rate` will not change due to 
    condition failure in logic. However, eventually, the delivered date will be less than the current time, causing 
    it to be considered as completed on time delivery  even though it is a late delivery. Since there is no field to 
    store the actual delivery date, it will misguide the `on_time_delivery_rate`. Therefore, in order to calculate 
    the `on_time_delivery_rate` in this scenario, we need to add an extra field named `delivered_date` (actual).
    '''
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()  # expected delivery date
    delivered_date = models.DateField(
        null=True, blank=True)  # Actual delivery date
    items = models.JSONField()
    quantity = models.IntegerField()
    # status = models.CharField(max_length=50)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"


@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    """
    Update vendor performance metrics after a PurchaseOrder is modified.

    Args:
        sender: The model class.
        instance: The actual instance being saved.
        created: Boolean flag indicating if the instance was newly created.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """

    vendor = instance.vendor

    if instance.status == 'completed':
        # Calculate on_time_delivery_rate
        completed_pos = PurchaseOrder.objects.filter(
            vendor=vendor, status='completed')
        total_completed_pos = completed_pos.count()
        on_time_deliveries = completed_pos.filter(
            delivered_date__lte=F('delivery_date')).count()
        on_time_delivery_rate = (
            on_time_deliveries / total_completed_pos) * 100 if total_completed_pos != 0 else 0
        vendor.on_time_delivery_rate = on_time_delivery_rate

        # Calculate fulfillment_rate
        total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
        fulfilled_pos = PurchaseOrder.objects.filter(
            vendor=vendor, quality_rating__gt=0.0, status='completed').count()
        vendor.fulfillment_rate = (
            fulfilled_pos / total_pos) * 100 if total_pos != 0 else 0

        # Calculate quality_rating_avg
        quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False, status='completed').aggregate(
            Avg('quality_rating'))['quality_rating__avg'] or 0
        vendor.quality_rating_avg = quality_rating_avg

    # Calculate average_response_time
    response_times = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False, issue_date__isnull=False).annotate(
        response_time=F('acknowledgment_date') - F('issue_date')).aggregate(Avg('response_time'))['response_time__avg']
    if response_times is not None:
        response_time_seconds = response_times.total_seconds()
        #average_response_time in hours
        vendor.average_response_time = round(response_time_seconds / 3600, 2)
    else:
        vendor.average_response_time = 0

    vendor.save()

    # Create historical performance record
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )
