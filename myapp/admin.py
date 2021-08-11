from django.contrib import admin

# Register your models here.
from myapp.models import Profile, Category, Listing

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Listing)