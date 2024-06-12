from django.db.models.signals import pre_save
from django.utils.text import slugify
from djongo import models
# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'authors'
        ordering = ['name']

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'publishers'
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']


class Book(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField(upload_to='book-image/', blank=True)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ArrayReferenceField(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING, related_name='books')
    publisher = models.ForeignKey(Publisher, on_delete=models.DO_NOTHING, related_name='books')

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']

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


pre_save.connect(pre_save_slug, sender=Book)
pre_save.connect(pre_save_slug, sender=Category)
pre_save.connect(pre_save_slug, sender=Author)
pre_save.connect(pre_save_slug, sender=Publisher)