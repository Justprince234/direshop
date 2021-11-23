from django.db import models
from accounts.models import User
from django_countries.fields import CountryField
from django.urls import reverse
from  django.conf import settings

# Create your models here.
CATERGORY_CHOICES = (
    ('SB', 'Skin and Beauty Products'),
    ('HP', 'Health Products'),
    ('M', 'Machines'),
)

class Item(models.Model):
    """Creates a database instance Item in database."""
    item_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, unique=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    category = models.CharField(choices=CATERGORY_CHOICES, max_length=2)
    description = models.TextField()
    price = models.FloatField()
    membership_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.item_name

    def get_add_to_cart_url(self):
        return reverse('store:add-to-cart', kwargs={'slug':self.slug})

    def get_remove_from_cart_url(self):
        return reverse('store:remove-from-cart', kwargs={'slug':self.slug})



class OrderItem(models.Model):
    """Creates a database instance OrderItem in database."""
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
        
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_membership_item_price(self):
        return self.quantity * self.item.membership_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_membership_item_price()

    def get_final_price(self):
        if self.item.membership_price:
            return self.get_membership_item_price()
        return self.get_total_item_price()

class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class CheckoutAddress(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    apartment_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = CountryField(multiple=False, blank_label='(select country)')
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    paypal_id = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    