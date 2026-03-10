from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
    ]    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f'Order {self.id} - {self.customer.name}'
    
class PrintJob(models.Model):
    JOB_TYPE_CHOICES = [
        # Marketing Materials
        ('flyer', 'Flyer'),
        ('poster', 'Poster'),
        ('brochure', 'Brochure'),
        ('booklet', 'Booklet'),
        ('catalog', 'Catalog'),
        
        # Corporate Stationery
        ('business_card', 'Business Card'),
        ('letterhead', 'Letterhead'),
        ('envelope', 'Envelope'),
        ('folder', 'Presentation Folder'),
        
        # Large Format & Signage
        ('banner', 'Vinyl Banner'),
        ('sticker', 'Sticker/Label'),
        ('pull_up', 'Pull-up Banner'),
        ('id_card', 'PVC ID Card'),
        
        # Apparel & Promotional
        ('tshirt', 'T-Shirt Print'),
        ('hoodie', 'Hoodie Print'),
        ('mug', 'Branded Mug'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="jobs")
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2) # Increased max_digits for large orders
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.job_type} ({self.quantity})"
    
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    full_name = models.CharField(max_length=150, help_text="Enter the user's official name")
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True, help_text="For automated job notifications")
 
    profile_picture = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True)
    bio = models.TextField(max_length=500, blank=True)

    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return f"{self.full_name} (@{self.username})"       
    
class Employee(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('designer', 'Designer'),
        ('editor', 'Editor'),
        ('printer', 'Printer'),
        ('finisher', 'Finisher'),
        ('delivery', 'Delivery Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)       
    
    def __str__(self):
        return f'{self.user.name} ({self.role})'
    
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    job = models.ForeignKey(PrintJob, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"    