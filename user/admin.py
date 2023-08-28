from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display =  [f.name for f in Profile._meta.get_fields()]
admin.site.register(Profile, ProfileAdmin)