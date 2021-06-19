from django.contrib import admin
from .models import Category, Donation, Institution

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
