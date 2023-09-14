from django.contrib import admin
from .models import Profile, CustomUser
# Register your models here.



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', "roles", 'is_staff', 'is_superuser']
admin.site.register(CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Profile._meta.get_fields()]
admin.site.register(Profile, ProfileAdmin)


# class MLAAdmin(admin.ModelAdmin):
#     list_display =  [f.name for f in MLA._meta.get_fields()]
# admin.site.register(MLA, MLAAdmin)