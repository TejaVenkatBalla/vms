from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_vendor_notification_email
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.http import HttpResponse

class RegisterView(APIView):
    def post(self, request):
        # Validate and serialize user data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Create user and generate JWT tokens
            user = serializer.save()

            # Create JWT token pair (access and refresh)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the tokens as response
            return Response({
                "message": "User Successfully Registered",
                'refresh': str(refresh),
                'access': access_token,
            }, status=status.HTTP_201_CREATED)

        # If validation fails, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vendor views
class VendorListCreate(generics.ListCreateAPIView):
    """
    A view for listing and creating Vendor objects.

    This view supports listing all Vendor objects and creating new Vendor objects.

    Authentication:
    - TokenAuthentication: The user must be authenticated with a valid token.

    Permissions:
    - IsAuthenticated: Only authenticated users are allowed access.

    Attributes:
    - permission_classes (list): List of permission classes.
    - queryset (QuerySet): Queryset of all Vendor objects.
    - serializer_class (Serializer): Serializer class for Vendor objects.
    """

    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting individual Vendor objects.

    This view supports retrieving, updating, and deleting individual Vendor objects by their unique identifier.

    Authentication:
    - TokenAuthentication: The user must be authenticated with a valid token.

    Permissions:
    - IsAuthenticated: Only authenticated users are allowed access.

    Attributes:
    - permission_classes (list): List of permission classes.
    - queryset (QuerySet): Queryset of all Vendor objects.
    - serializer_class (Serializer): Serializer class for Vendor objects.
    """

    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    """
    Retrieve performance metrics for a specific vendor.

    This function retrieves performance metrics for a vendor identified by the given vendor_id.

    Parameters:
    - request: The HTTP request object.
    - vendor_id (int): The unique identifier of the vendor.

    Returns:
    - Response: A JSON response containing the performance metrics of the vendor.

    Raises:
    - HTTP 404: If the vendor with the specified ID does not exist.
    """
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    performance_metrics = {
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate
    }
    # optional to insert data
    HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )

    return Response(performance_metrics)

# Purchase order views
class PurchaseOrderListCreate(generics.ListCreateAPIView):
    """
    A view for listing and creating Purchase Order objects.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id:
            return PurchaseOrder.objects.filter(vendor__id=vendor_id)
        return PurchaseOrder.objects.all()

    def perform_create(self, serializer):
        """
        Save the Purchase Order and send a notification email to the vendor.
        """
        # Save the purchase order instance
        purchase_order = serializer.save()

        # Retrieve vendor details
        vendor = purchase_order.vendor
        vendor_email = vendor.email # Assuming 'email' is in contact_details
        vendor_name = vendor.name

        # Compose the email
        subject = f"New Purchase Order Issued: {purchase_order.po_number}"
        message = (
            f"Dear {vendor_name},\n\n"
            f"A new Purchase Order (PO#{purchase_order.po_number}) has been issued to you on {purchase_order.order_date}.\n\n"
            f"Order Details:\n"
            f"- Items: {purchase_order.items}\n"
            f"- Delivery Date: {purchase_order.delivery_date}\n\n"
            f"Please acknowledge this order at your earliest convenience.\n\n"
            f"Best regards,\n[Vendor Management System]"
        )

        # Trigger the Celery task to send the email
        if vendor_email:
            send_vendor_notification_email.delay(vendor_email, subject, message)


class PurchaseOrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting individual PurchaseOrder objects.

    This view supports retrieving, updating, and deleting individual PurchaseOrder objects by their unique identifier.

    Authentication:
    - TokenAuthentication: The user must be authenticated with a valid token.

    Permissions:
    - IsAuthenticated: Only authenticated users are allowed access.

    Attributes:
    - permission_classes (list): List of permission classes.
    - queryset (QuerySet): Queryset of all PurchaseOrder objects.
    - serializer_class (Serializer): Serializer class for PurchaseOrder objects.
    """
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    """
    Acknowledge a purchase order.

    This function acknowledges a purchase order identified by the given po_id.

    Parameters:
    - request: The HTTP request object.
    - po_id (int): The unique identifier of the purchase order.

    Returns:
    - Response: A JSON response indicating the success or failure of the acknowledgment.

    Raises:
    - HTTP 404: If the purchase order with the specified ID does not exist.
    """
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()

    return Response({'message': 'Purchase Order acknowledged successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def schedule_task(request):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=interval,
        name="deadline-scheduler_01",
        task="myapp.tasks.send_delivery_deadline_reminders",
    )

    return HttpResponse("Task scheduled!")