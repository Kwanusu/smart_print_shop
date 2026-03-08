"""
URL configuration for smart_print_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Smart Print management APIs",
        default_version='v0.1.0',
        description="The Smart Print API provides endpoints to manage the full lifecycle of a printing business. It enables seamless integration of customer management, order tracking, print job handling, employee role assignment, and activity logging.\n\nKey Features\nCustomer Management: Create, update, and retrieve customer records.\n\nOrder Tracking: Manage orders, statuses (pending, in_production, completed, delivered), and pricing.\n\nPrint Jobs: Define job types (flyers, posters, banners, apparel, etc.), quantities, and production status.\n\nUser & Employee Management: Extend Django's User model with employee roles (admin, designer, printer, delivery staff).\n\nActivity Logs: Record user actions for auditing and accountability.\n\nAuthentication\nToken-based authentication (JWT or DRF TokenAuth).\n\nRequired for most endpoints to ensure secure access.\n\nAvailable Endpoints\n/api/customers/ → Manage customers\n\n/api/orders/ → Manage orders and statuses\n\n/api/jobs/ → Manage print jobs linked to orders\n\n/api/users/ → Manage system users\n\n/api/employees/ → Assign and manage employee roles\n\n/api/logs/ → Track activity logs"
    ),
    public=True,
    permission_classes=[permissions.AllowAny,]
)

path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0, name='schema-swagger-ui'))
path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0, name='schema-redoc'))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('print_shop.urls'))
]
