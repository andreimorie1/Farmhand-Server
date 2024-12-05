from django.contrib import admin

from django.contrib import admin
from .models import Farmer

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname')
    search_fields = ('id', 'firstname', 'lastname')