from rest_framework import viewsets
from .models import Customer, Order, PrintJob, User, Employee, ActivityLog
from .serializers import (
    CustomerSerializer, 
    OrderSerializer, 
    PrintJobSerializer, 
    UserSerializer, 
    EmployeeSerializer, 
    ActivityLogSerializer)

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
class PrintJobViewSet(viewsets.ModelViewSet):
    queryset = PrintJob.objects.all()
    serializer_class = PrintJobSerializer
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer

