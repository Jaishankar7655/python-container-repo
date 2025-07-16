from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre', 'available', 'created_at']
    list_filter = ['genre', 'available', 'created_at']
    search_fields = ['title', 'author', 'isbn']
    list_editable = ['available']
    readonly_fields = ['created_at', 'updated_at']