from django.contrib import admin

from .models import Product, Vote

# Register your models here.

admin.site.register((Product, Vote))