from django.contrib import admin

from .models import Addon, MenuItem, Category, PiOrder, OrderItem

# Register your models here.

admin.site.register(MenuItem)
admin.site.register(Addon)
admin.site.register(Category)
admin.site.register(PiOrder)
admin.site.register(OrderItem)