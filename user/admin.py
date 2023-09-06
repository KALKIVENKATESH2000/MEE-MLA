from django.contrib import admin
from .models import Profile, MLA, CustomUser
# Register your models here.



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'fcm_token', 'is_staff']
admin.site.register(CustomUser, CustomUserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Profile._meta.get_fields()]
admin.site.register(Profile, ProfileAdmin)


class MLAAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in MLA._meta.get_fields()]
admin.site.register(MLA, MLAAdmin)