from django.contrib import admin
from .models import *


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username', 'password']


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'name']


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user']


@admin.register(Chattings)
class ChattingsAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'user', 'message', 'date']
