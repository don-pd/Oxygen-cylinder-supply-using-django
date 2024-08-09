# booking_forms.py
from django import forms
from .models import Booking
from .models import Product, ProductQuantity, UserProfile

class ProductForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=0, required=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity']

    def save(self, commit=True, manufacturer=None):
        product = super().save(commit=False)
        product_quantity = self.cleaned_data['quantity']
        if commit:
            product.save()
            if manufacturer:
                product_quantity = self.cleaned_data.get('quantity')
                ProductQuantity.objects.create(product=product, manufacturer=manufacturer, quantity=product_quantity)
        return product

class BookingForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),  # Ensure that Product objects are correctly populated
        label='Select Product'
    )
    manufacturer = forms.ModelChoiceField(
        queryset=UserProfile.objects.filter(usertype='manufacturer'),  # Ensure this filter matches your data
        label='Select Manufacturer'
    )
    quantity = forms.IntegerField(
        min_value=1,  # Ensure quantity must be at least 1
        label='Quantity'
    )