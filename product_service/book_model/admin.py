from django.contrib import admin
from django.utils.html import mark_safe

from .models import Book, Category, Publisher, Author

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'created_at', 'updated_at']
    list_display_links = ['name']
    search_fields = ['name', 'id']
    ordering = ['-created_at']
    readonly_fields = ['cover']

    def cover(self, book):
        return mark_safe("<img src='{img_url}' alt='{alt}' width='320px' />".format(img_url=book.image_url, alt=book.name))


admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Author)
