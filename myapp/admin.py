from django.contrib import admin

from myapp.models import Order, Customer, Product

# Register your models here.
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Product)
