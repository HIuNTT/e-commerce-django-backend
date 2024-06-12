from django.db.models.signals import pre_save
from django.utils.text import slugify
from djongo import models

# Create your models here.


class Style(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, default='')

    class Meta:
        db_table = 'clothes_styles'
        ordering = ['name']

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clothes_producers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Clothes(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField(upload_to='clothes-image/', blank=True)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='clothes')
    style = models.ForeignKey(Style, on_delete=models.SET_NULL, null=True, related_name='clothes')

    class Meta:
        db_table = 'clothes'
        ordering = ['name']

    def __str__(self):
        return self.name

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    @property
    def image_url(self):
        return (
            f"https://res.cloudinary.com/dk8ngubis/{self.image}"
        )


def pre_save_slug(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    instance.slug = slug


pre_save.connect(pre_save_slug, sender=Style)
pre_save.connect(pre_save_slug, sender=Producer)
pre_save.connect(pre_save_slug, sender=Clothes)
