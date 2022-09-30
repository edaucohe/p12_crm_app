from django.contrib import admin
from contracts.models import Contract


@admin.register(Contract)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'payment_due', 'status', 'customer', 'user')


# admin.site.register(Contract)
