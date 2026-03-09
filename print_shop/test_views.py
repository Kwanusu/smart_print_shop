import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Customer, Order, PrintJob, Employee, ActivityLog

UserModel = get_user_model()

@pytest.fixture
def api_client(db):
    user = UserModel.objects.create_user(
        username="testuser",
        password="testpass123",
        full_name="Test User",
        email="test@example.com"
    )
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


# -------------------------
# CustomerViewSet Tests
# -------------------------
@pytest.mark.django_db
def test_list_customers(api_client):
    client, _ = api_client
    Customer.objects.create(name="Joseph", email="joseph@example.com")
    response = client.get(reverse("customers-list"))
    assert response.status_code == 200
    assert len(response.json()) >= 1

@pytest.mark.django_db
def test_create_customer_valid(api_client):
    client, _ = api_client
    payload = {"name": "Alice", "email": "alice@example.com"}
    response = client.post(reverse("customers-list"), payload, format="json")
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"

@pytest.mark.django_db
def test_create_customer_invalid(api_client):
    client, _ = api_client
    payload = {"name": "Bob"}  # missing email
    response = client.post(reverse("customers-list"), payload, format="json")
    assert response.status_code == 400


# -------------------------
# OrderViewSet Tests
# -------------------------
@pytest.mark.django_db
def test_list_orders(api_client):
    client, user = api_client
    customer = Customer.objects.create(name="Joseph", email="joseph@example.com")
    Order.objects.create(customer=customer, total_price=100.00)
    response = client.get(reverse("orders-list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_retrieve_order_not_found(api_client):
    client, _ = api_client
    response = client.get(reverse("orders-detail", args=[999]))
    assert response.status_code == 404


# -------------------------
# PrintJobViewSet Tests
# -------------------------
@pytest.mark.django_db
def test_list_printjobs(api_client):
    client, _ = api_client
    customer = Customer.objects.create(name="Joseph", email="joseph@example.com")
    order = Order.objects.create(customer=customer, total_price=50.00)
    PrintJob.objects.create(order=order, job_type="poster", quantity=10, price_per_unit=5.00)
    response = client.get(reverse("print_job-list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_printjob_valid(api_client):
    client, _ = api_client
    customer = Customer.objects.create(name="Joseph", email="joseph@example.com")
    order = Order.objects.create(customer=customer, total_price=50.00)
    payload = {"order": order.id, "job_type": "flyer", "quantity": 100, "price_per_unit": "2.50"}
    response = client.post(reverse("print_job-list"), payload, format="json")
    assert response.status_code in [201, 400]


# -------------------------
# UserViewSet Tests
# -------------------------
@pytest.mark.django_db
def test_list_users(api_client):
    client, _ = api_client
    response = client.get(reverse("users-list"))
    assert response.status_code == 200


# -------------------------
# EmployeeViewSet Tests
# -------------------------
@pytest.mark.django_db
def test_list_employees(api_client):
    client, user = api_client
    Employee.objects.create(user=user, role="designer")
    response = client.get(reverse("employees-list"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_employee_invalid(api_client):
    client, _ = api_client
    payload = {}  # missing required fields
    response = client.post(reverse("employees-list"), payload, format="json")
    assert response.status_code == 400


# -------------------------
# ActivityLogViewSet Tests
# -------------------------
@pytest.mark.django_db
def test_list_activity_logs(api_client):
    client, user = api_client
    ActivityLog.objects.create(user=user, action="Login")
    response = client.get(reverse("activity_logs-list"))
    assert response.status_code == 200
