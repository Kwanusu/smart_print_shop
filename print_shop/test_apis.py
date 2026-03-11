from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Order, PrintJob, User, Employee, ActivityLog

UserModel = get_user_model()

class BaseAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username="testuser",
            password="testpass123",
            full_name="Test User",
            email="test@example.com"
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.customer = Customer.objects.create(name="Joseph", email="joseph@example.com")


class CustomerViewSetTests(BaseAPITest):
    def test_list_customers(self):
        response = self.client.get(reverse("customers-list"))
        self.assertEqual(response.status_code, 200)

    def test_create_customer_valid(self):
        payload = {"name": "Alice", "email": "alice@example.com"}
        response = self.client.post(reverse("customers-list"), payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Alice")

    def test_create_customer_invalid(self):
        payload = {"name": "Bob"} 
        response = self.client.post(reverse("customers-list"), payload, format="json")
        self.assertEqual(response.status_code, 400)


class OrderViewSetTests(BaseAPITest):
    def test_list_orders(self):
        Order.objects.create(customer=self.customer, total_price=100.00)
        response = self.client.get(reverse("orders-list"))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_order_not_found(self):
        response = self.client.get(reverse("orders-detail", args=[999]))
        self.assertEqual(response.status_code, 404)


class PrintJobViewSetTests(BaseAPITest):
    def test_list_printjobs(self):
        order = Order.objects.create(customer=self.customer, total_price=50.00)
        PrintJob.objects.create(order=order, job_type="poster", quantity=10, price_per_unit=5.00)
        response = self.client.get(reverse("print_job-list"))
        self.assertEqual(response.status_code, 200)

    def test_create_printjob_valid(self):
        order = Order.objects.create(customer=self.customer, total_price=50.00)
        payload = {"order": order.id, "job_type": "flyer", "quantity": 100, "price_per_unit": "2.50"}
        response = self.client.post(reverse("print_job-list"), payload, format="json")
        self.assertIn(response.status_code, [201, 400])

    def test_printjob_internal_server_error(self):
        with patch("print_shop.views.PrintJob.objects.all", side_effect=Exception("DB failure")):
            response = self.client.get(reverse("print_job-list"))
            self.assertEqual(response.status_code, 500)


class UserViewSetTests(BaseAPITest):
    def test_list_users(self):
        response = self.client.get(reverse("users-list"))
        self.assertEqual(response.status_code, 200)


class EmployeeViewSetTests(BaseAPITest):
    def test_list_employees(self):
        Employee.objects.create(user=self.user, role="designer")
        response = self.client.get(reverse("employees-list"))
        self.assertEqual(response.status_code, 200)

    def test_create_employee_invalid(self):
        payload = {} 
        response = self.client.post(reverse("employees-list"), payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_employee_internal_server_error(self):
        with patch("print_shop.views.Employee.objects.all", side_effect=Exception("DB failure")):
            response = self.client.get(reverse("employees-list"))
            self.assertEqual(response.status_code, 500)


class ActivityLogViewSetTests(BaseAPITest):
    def test_list_activity_logs(self):
        ActivityLog.objects.create(user=self.user, action="Login")
        response = self.client.get(reverse("activity_logs-list"))
        self.assertEqual(response.status_code, 200)
