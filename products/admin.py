from django.contrib import admin

# Register your models here.
from products.models import *
admin.site.register(Box)
admin.site.register(Count)

