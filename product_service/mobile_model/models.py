from django.db.models.signals import pre_save
from django.utils.text import slugify
from djongo import models
# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mobile_types'


class Producer(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mobile_producers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Mobile(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField(upload_to='mobiles-image/', blank=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True, related_name='mobiles')
    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True, related_name='mobiles')
    ram = models.CharField(max_length=255)
    memory = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mobiles'
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


pre_save.connect(pre_save_slug, sender=Producer)
pre_save.connect(pre_save_slug, sender=Mobile)
pre_save.connect(pre_save_slug, sender=Type)
