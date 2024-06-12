from django.db import models


# Create your models here.


class CartItem(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('mobile', 'Mobile'),
        ('book', 'Book'),
        ('clothes', 'Clothes'),
    ]

    user_id = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    product_id = models.IntegerField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)

    class Meta:
        db_table = 'cart_items'
        ordering = ['date_added']
