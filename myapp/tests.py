from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timezone
from .models import *


class VendorAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_create_vendor(self):
        url = reverse('vendor-list')
        vendor_data = {
            'name': 'Test Vendor',
            'contact_details': 'Contact Details',
            'address': 'Test Address',
            'vendor_code': '12345'
            # Add other required fields
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url, vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_vendor = Vendor.objects.last()
        self.assertEqual(created_vendor.name, vendor_data['name'])
        self.assertEqual(created_vendor.contact_details,
                         vendor_data['contact_details'])
        self.assertEqual(created_vendor.address, vendor_data['address'])
        self.assertEqual(created_vendor.vendor_code,
                         vendor_data['vendor_code'])

    def test_create_vendor_missing_fields(self):
        url = reverse('vendor-list')
        vendor_data = {
            'name': 'Test Vendor',
            'address': 'Test Address',
            'vendor_code': '12345'
            # Missing 'contact_details' field
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url, vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_vendors(self):
        url = reverse('vendor-list')
        Vendor.objects.create(
            name='Vendor 1', contact_details='...', address='...', vendor_code='c1')
        Vendor.objects.create(
            name='Vendor 2', contact_details='...', address='...', vendor_code='c2')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Vendor.objects.count())

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(
            name='Test Vendor', contact_details='...', address='...', vendor_code='...')
        url = reverse('vendor-detail', kwargs={'pk': vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], vendor.name)
        self.assertEqual(
            response.data['contact_details'], vendor.contact_details)
        self.assertEqual(response.data['address'], vendor.address)
        self.assertEqual(response.data['vendor_code'], vendor.vendor_code)

    def test_retrieve_nonexistent_vendor(self):
        non_existent_vendor_id = 9999
        url = reverse('vendor-detail', kwargs={'pk': non_existent_vendor_id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_vendor(self):
        vendor = Vendor.objects.create(
            name='Test Vendor', contact_details='...', address='...', vendor_code='...')
        url = reverse('vendor-detail', kwargs={'pk': vendor.pk})
        new_vendor_data = {
            'name': 'Updated Vendor Name',
            'contact_details': 'Updated Contact Details',
            'address': 'Updated Address',
            'vendor_code': '54321'
            # Add other fields for update
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(url, new_vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_vendor = Vendor.objects.get(pk=vendor.pk)
        self.assertEqual(updated_vendor.name, new_vendor_data['name'])
        self.assertEqual(updated_vendor.contact_details,
                         new_vendor_data['contact_details'])
        self.assertEqual(updated_vendor.address, new_vendor_data['address'])
        self.assertEqual(updated_vendor.vendor_code,
                         new_vendor_data['vendor_code'])

    def test_update_vendor_invalid_data(self):
        vendor = Vendor.objects.create(
            name='Test Vendor', contact_details='...', address='...', vendor_code='...')
        url = reverse('vendor-detail', kwargs={'pk': vendor.pk})
        invalid_data = {
            'name': '',  # Invalid empty name
            'contact_details': 'Updated Contact Details',
            'address': 'Updated Address',
            'vendor_code': '54321'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_vendor(self):
        vendor = Vendor.objects.create(
            name='Test Vendor', contact_details='...', address='...', vendor_code='...')
        url = reverse('vendor-detail', kwargs={'pk': vendor.pk})
        initial_count = Vendor.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), initial_count - 1)

    def test_delete_nonexistent_vendor(self):
        non_existent_vendor_id = 9999
        url = reverse('vendor-detail', kwargs={'pk': non_existent_vendor_id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vendor_performance(self):
        vendor = Vendor.objects.create(name='Test Vendor', on_time_delivery_rate=0.9,
                                       contact_details='Contact Details', address='Test Address',
                                       vendor_code='12345', quality_rating_avg=4.5,
                                       average_response_time=2.3, fulfillment_rate=0.95)
        url = reverse('vendor-performance', kwargs={'vendor_id': vendor.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['on_time_delivery_rate'], vendor.on_time_delivery_rate)
        self.assertEqual(
            response.data['quality_rating_avg'], vendor.quality_rating_avg)
        self.assertEqual(
            response.data['average_response_time'], vendor.average_response_time)
        self.assertEqual(
            response.data['fulfillment_rate'], vendor.fulfillment_rate)
        self.assertEqual(HistoricalPerformance.objects.count(), 1)
        created_performance = HistoricalPerformance.objects.last()
        self.assertEqual(created_performance.vendor, vendor)
        self.assertAlmostEqual(
            created_performance.on_time_delivery_rate, vendor.on_time_delivery_rate)
        self.assertAlmostEqual(
            created_performance.quality_rating_avg, vendor.quality_rating_avg)
        self.assertAlmostEqual(
            created_performance.average_response_time, vendor.average_response_time)
        self.assertAlmostEqual(
            created_performance.fulfillment_rate, vendor.fulfillment_rate)

    def test_vendor_performance_without_authentication(self):
        vendor = Vendor.objects.create(name='Test Vendor', on_time_delivery_rate=0.9,
                                       contact_details='Contact Details', address='Test Address',
                                       vendor_code='12345', quality_rating_avg=4.5,
                                       average_response_time=2.3, fulfillment_rate=0.95)
        url = reverse('vendor-performance', kwargs={'vendor_id': vendor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PurchaseOrderAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.vendor = Vendor.objects.create(
            name='Test Vendor', contact_details='...', address='...', vendor_code='123')
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=datetime.now(timezone.utc),
            delivery_date=datetime.now(timezone.utc),
            items=[{'item_name': 'Item 1', 'quantity': 10}],
            quantity=10,
            status='pending',
            issue_date=datetime.now(timezone.utc),
        )
        self.purchase_order_url = reverse(
            'purchaseorder-detail', args=[self.purchase_order.pk])
        self.list_create_url = reverse('purchaseorder-list')
        self.acknowledge_url = reverse(
            'acknowledge-purchaseorder', args=[self.purchase_order.pk])

    def test_list_purchase_orders(self):
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), PurchaseOrder.objects.count())

    def test_create_purchase_order(self):
        initial_count = PurchaseOrder.objects.count()
        new_purchase_order_data = {
            'po_number': 'PO456',
            'vendor': self.vendor.pk,
            'order_date': datetime.now(timezone.utc),
            'delivery_date': datetime.now(timezone.utc),
            'items': [{'item_name': 'Item 2', 'quantity': 20}],
            'quantity': 20,
            'status': 'pending',
            'issue_date': datetime.now(timezone.utc),
        }
        response = self.client.post(
            self.list_create_url, new_purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), initial_count + 1)
        created_purchase_order = PurchaseOrder.objects.last()
        self.assertEqual(created_purchase_order.po_number,
                         new_purchase_order_data['po_number'])
        self.assertEqual(created_purchase_order.vendor_id, self.vendor.pk)
        self.assertEqual(created_purchase_order.order_date,
                         new_purchase_order_data['order_date'])
        self.assertEqual(created_purchase_order.delivery_date,
                         new_purchase_order_data['delivery_date'])
        self.assertEqual(created_purchase_order.items,
                         new_purchase_order_data['items'])
        self.assertEqual(created_purchase_order.quantity,
                         new_purchase_order_data['quantity'])
        self.assertEqual(created_purchase_order.status,
                         new_purchase_order_data['status'])
        self.assertEqual(created_purchase_order.issue_date,
                         new_purchase_order_data['issue_date'])

    def test_create_purchase_order_missing_fields(self):
        initial_count = PurchaseOrder.objects.count()
        new_purchase_order_data = {
            # Missing 'po_number' field
            'vendor': self.vendor.pk,
            'order_date': datetime.now(timezone.utc),
            'delivery_date': datetime.now(timezone.utc),
            'items': [{'item_name': 'Item 2', 'quantity': 20}],
            'quantity': 20,
            'status': 'pending',
            'issue_date': datetime.now(timezone.utc),
        }
        response = self.client.post(
            self.list_create_url, new_purchase_order_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PurchaseOrder.objects.count(), initial_count)

    def test_filter_purchase_orders_by_vendor_id(self):
        response = self.client.get(self.list_create_url, {
                                   'vendor_id': self.vendor.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_purchase_order(self):
        response = self.client.get(self.purchase_order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'],
                         self.purchase_order.po_number)

    def test_retrieve_nonexistent_purchase_order(self):
        non_existent_po_id = 9999
        url = reverse('purchaseorder-detail', args=[non_existent_po_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_purchase_order(self):
        updated_po_number = 'PO456'
        updated_order_date = datetime.now(timezone.utc)
        data = {
            'po_number': updated_po_number,
            'vendor': self.vendor.pk,
            'order_date': updated_order_date,
            'delivery_date': self.purchase_order.delivery_date,
            'items': self.purchase_order.items,
            'quantity': self.purchase_order.quantity,
            'status': self.purchase_order.status,
            'issue_date': self.purchase_order.issue_date,
        }
        response = self.client.put(
            self.purchase_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.po_number, updated_po_number)
        self.assertEqual(self.purchase_order.order_date, updated_order_date)

    def test_update_nonexistent_purchase_order(self):
        non_existent_po_id = 9999
        url = reverse('purchaseorder-detail', args=[non_existent_po_id])
        data = {
            'po_number': 'PO456',
            'vendor': self.vendor.pk,
            'order_date': datetime.now(timezone.utc),
            'delivery_date': datetime.now(timezone.utc),
            'items': [{'item_name': 'Item 2', 'quantity': 20}],
            'quantity': 20,
            'status': 'pending',
            'issue_date': datetime.now(timezone.utc),
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_purchase_order_invalid_data(self):
        updated_po_number = ''  # Invalid empty po_number
        updated_order_date = datetime.now(timezone.utc)
        data = {
            'po_number': updated_po_number,
            'vendor': self.vendor.pk,
            'order_date': updated_order_date,
            'delivery_date': self.purchase_order.delivery_date,
            'items': self.purchase_order.items,
            'quantity': self.purchase_order.quantity,
            'status': self.purchase_order.status,
            'issue_date': self.purchase_order.issue_date,
        }
        response = self.client.put(
            self.purchase_order_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_purchase_order(self):
        response = self.client.delete(self.purchase_order_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PurchaseOrder.objects.filter(
            pk=self.purchase_order.pk).exists())

    def test_delete_nonexistent_purchase_order(self):
        non_existent_po_id = 9999
        url = reverse('purchaseorder-detail', args=[non_existent_po_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_acknowledge_existing_purchase_order(self):
        response = self.client.post(self.acknowledge_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertIsNotNone(self.purchase_order.acknowledgment_date)

    def test_acknowledge_non_existing_purchase_order(self):
        non_existing_po_id = 9999
        url = reverse('acknowledge-purchaseorder', args=[non_existing_po_id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_acknowledge_purchase_order_without_authentication(self):
        self.client.credentials()  # Clear authentication credentials
        response = self.client.post(self.acknowledge_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
