from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import CustomUser, Branch, Zone, HeadOffice


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('Phone_number', 'Phone_is_verified', 'otp', 'ACCESS_LEVEL_CHOICES',
                    'access_level', 'branch', 'zone', 'head_office', 'USERNAME_FIELD', )


@admin.register(HeadOffice)
class HeadOfficeAdmin(admin.ModelAdmin):
    list_display = ('HeadOffice_name', )


admin.site.register(Branch)
admin.site.register(Zone)
