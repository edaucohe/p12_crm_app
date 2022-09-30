"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import SignUpViewSet, UserViewSet
from customers.views import CustomerViewSet
from contracts.views import ContractViewSet
from events.views import EventViewSet

router = DefaultRouter()
# /users/   ||   /users/{id}/
router.register(r'users', UserViewSet, basename='users')
# /customers/   ||   /customers/{id}/
router.register(r'customers', CustomerViewSet, basename='customers')

# /customers/{id}/contracts/   ||   /customers/{id}/contracts/{id}
customer_router = routers.NestedSimpleRouter(router, r'customers', lookup='customers')
customer_router.register(r'contracts', ContractViewSet, basename='contracts')

# /customers/{id}/contracts/{id}/events/   ||   /customers/{id}/contracts/{id}/events/{id}/
# contract_router = routers.NestedSimpleRouter(customer_router, r'contracts', lookup='contracts')
customer_router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signup/', SignUpViewSet.as_view(), name='signup'),
    path(r'', include(router.urls)),
    path(r'', include(customer_router.urls)),
    # path(r'', include(contract_router.urls)),
]
