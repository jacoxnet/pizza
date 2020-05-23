from django.contrib import admin

from .models import Addon, MenuItem, Customer, Order

# Register your models here.

admin.site.register(MenuItem)
admin.site.register(Addon)
admin.site.register(Customer)
admin.site.register(Order)