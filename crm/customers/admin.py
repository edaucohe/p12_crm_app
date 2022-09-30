from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'company_name', 'user', 'status')


# admin.site.register(Customer)
