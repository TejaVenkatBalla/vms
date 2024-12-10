from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    #signin/signup
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Vendor URLs
    path('api/vendors/', views.VendorListCreate.as_view(), name='vendor-list'),
    path('api/vendors/<int:pk>/',
         views.VendorRetrieveUpdateDestroy.as_view(), name='vendor-detail'),

    # Vendor Performance Endpoint
    path('api/vendors/<int:vendor_id>/performance/',
         views.vendor_performance, name='vendor-performance'),

    # Purchase Order URLs
    path('api/purchase_orders/', views.PurchaseOrderListCreate.as_view(),
         name='purchaseorder-list'),
    path('api/purchase_orders/<int:pk>/',
         views.PurchaseOrderRetrieveUpdateDestroy.as_view(), name='purchaseorder-detail'),

    # Acknowledge Purchase Order
    path('api/purchase_orders/<int:po_id>/acknowledge/',
         views.acknowledge_purchase_order, name='acknowledge-purchaseorder'),
]
