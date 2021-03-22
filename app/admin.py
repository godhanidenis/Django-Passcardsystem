# -*- encoding: utf-8 -*-
"""
"""

from django.contrib import admin
from app.models import Residence, visitorType, visitorValidity, Visitor, Resident, Status, residenceType, visitorAccessTypes, appUserTypes, AppUser, residenceSyndics, residenceAreas, AppUserAssignedAreas, Inouts

admin.site.site_header = 'RACS administration'

admin.site.register(visitorType)
admin.site.register(visitorValidity)
admin.site.register(Status)
admin.site.register(residenceType)
admin.site.register(visitorAccessTypes)


class ResidenceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name', 'type']
admin.site.register(Residence, ResidenceAdmin)

class VisitorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['resident', 'residence_area', 'status']
admin.site.register(Visitor, VisitorAdmin)

class ResidentAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['residence_area']
admin.site.register(Resident, ResidentAdmin)

class appUserTypesAdmin(admin.ModelAdmin):
    search_fields = ['app_user_type'] 
admin.site.register(appUserTypes, appUserTypesAdmin)

class AppUserAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['usertype', 'accesstype']
admin.site.register(AppUser, AppUserAdmin)

class SyndicsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['residence']
admin.site.register(residenceSyndics, SyndicsAdmin)

class AreasAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['residence']
admin.site.register(residenceAreas, AreasAdmin)

class AppUserAreasAdmin(admin.ModelAdmin):
    search_fields = ['user', 'residence_area']
    list_filter = ['user', 'residence_area']
admin.site.register(AppUserAssignedAreas, AppUserAreasAdmin)


class InoutsAdmin(admin.ModelAdmin):
    list_filter = ['inoutpass']
admin.site.register(Inouts, InoutsAdmin)
