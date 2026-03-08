from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, OrderViewSet, PrintJobViewSet, UserViewSet, EmployeeViewSet, ActivityLogViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'print_job', PrintJobViewSet, basename='print_job')
router.register(r'users', UserViewSet, basename='users')
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'Activity_logs', ActivityLogViewSet, basename='activity_logs')

urlpatterns = [
    path('', include(router.urls)),
]
