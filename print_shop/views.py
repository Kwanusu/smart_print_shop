from rest_framework import viewsets, permissions
from .models import Customer, Order, PrintJob, User, Employee, ActivityLog
from .serializers import (
    CustomerSerializer, 
    OrderSerializer, 
    PrintJobSerializer, 
    UserSerializer, 
    EmployeeSerializer, 
    ActivityLogSerializer
)
from rest_framework.permissions import IsAuthenticated

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing customer instances.
    
    Access is restricted to authenticated users. This ViewSet provides 
    standard CRUD operations for the Customer model.
    """
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    
    Includes custom logic for ownership filtering and automatic 
    activity logging upon order creation.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Restricts the list of orders to only those belonging 
        to the currently authenticated customer user.
        """
        return Order.objects.filter(customer__user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Saves a new order instance and automatically creates an 
        associated ActivityLog entry for the current user.
        """
        order = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            action="Created Order",
            order=order
        )
    

class PrintJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling print job instances.
    
    Provides standard CRUD functionality for tracking specific 
    print tasks within the system.
    """
    queryset = PrintJob.objects.all()
    serializer_class = PrintJobSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing system user accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing employee data and roles.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

class ActivityLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing system activity logs.
    
    Used to audit actions like order creation. Access is 
    restricted to authenticated users.
    """ 
    queryset = ActivityLog.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityLogSerializer