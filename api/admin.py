from django.contrib import admin
from .models import State, District, Constituency, PollingStation

# Register your models here.

class StateAdmin(admin.ModelAdmin):
    list_display =   ['id', 'name']
admin.site.register(State, StateAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display =  ['id', 'state', 'name']
admin.site.register(District, DistrictAdmin)


class ConstituencyAdmin(admin.ModelAdmin):
    list_display =   ['id', 'district', 'name']
admin.site.register(Constituency, ConstituencyAdmin)

class PollingStationAdmin(admin.ModelAdmin):
    list_display =   ['id', 'constituency', 'no', 'name', 'location']
admin.site.register(PollingStation, PollingStationAdmin)