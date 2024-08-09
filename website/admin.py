from django.contrib import admin
from .models import  UserProfile, Product, ProductQuantity, Booking


admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(ProductQuantity)
admin.site.register(Booking)