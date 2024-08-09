from django.db import models
from django.contrib.auth.models import User
from datetime import date


 
class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('hospital', 'Hospital'),
        ('dispensary', 'Dispensary'),
        ('manufacturer', 'Manufacturer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=12, choices=USER_TYPE_CHOICES, default='user')

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    
    def __str__(self):
        return self.name

class ProductQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(UserProfile,  limit_choices_to={'usertype': 'manufacturer'},on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'manufacturer')
    
    def __str__(self):
        return f"{self.manufacturer.user.username} - {self.product.name}: {self.quantity}"




class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    

    def __str__(self):
        return f'{self.user.username} booked {self.quantity} of {self.product.name}'

       