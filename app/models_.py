# -*- encoding: utf-8 -*-
"""
"""

from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


from datetime import datetime
from time import strftime

import uuid 


from django.contrib.auth.hashers import make_password

import random



class residenceType(models.Model):
    residence_type = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.residence_type
    class Meta:
        verbose_name = 'Location Type'
        verbose_name_plural = 'Location Types'
 

class appUserTypes(models.Model):
    app_user_type = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.app_user_type
    class Meta:
        verbose_name = 'App User Type'
        verbose_name_plural = 'App User Type'


class visitorAccessTypes(models.Model):
    access_type = models.CharField(max_length=120, default='')
    main_account = models.CharField(max_length=120, default='')
    can_access_website = models.BooleanField(default=False)
    can_view_dashboard = models.BooleanField(default=False)
    can_view_users = models.BooleanField(default=False)
    can_edit_users = models.BooleanField(default=False)
    can_view_locations = models.BooleanField(default=False)
    can_edit_locations = models.BooleanField(default=False)
    can_view_connections = models.BooleanField(default=False)
    can_edit_connections = models.BooleanField(default=False)
    can_view_acces_types = models.BooleanField(default=False)
    can_edit_acces_types = models.BooleanField(default=False)
    can_view_visitor_types = models.BooleanField(default=False)
    can_edit_visitor_types = models.BooleanField(default=False)
    can_view_access_passes = models.BooleanField(default=False)
    can_edit_access_passes = models.BooleanField(default=False)
    can_monitor = models.BooleanField(default=False)
    def __str__(self):
        return self.access_type
    class Meta:
        verbose_name = 'Access Type'
        verbose_name_plural = 'Access Type'


class Residence(models.Model):
    
    name = models.CharField(max_length=140, default='')
    address = models.CharField(max_length=140, default='')
    contact_person = models.CharField(max_length=140, default='')
    contact_email = models.CharField(max_length=140, default='')
    contact_phone = models.CharField(max_length=140, default='')
    company = models.CharField(max_length=140, default='', null=True, blank=True)
    floor = models.CharField(max_length=140, default='', null=True, blank=True)
    type = models.ForeignKey(residenceType, null=True, related_name='residence_type_from', on_delete=models.CASCADE)
    user = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

class residenceSyndics(models.Model):
    residence = models.ForeignKey(Residence, null=True, related_name='residence_for_syndics', on_delete=models.CASCADE)
    syndics_name = models.CharField(max_length=140, default='')
    syndics_email = models.CharField(max_length=140, default='')
    syndics_phone = models.CharField(max_length=140, default='')
    def __str__(self):
        return self.syndics_name
    class Meta:
        verbose_name = 'Residence Syndic'
        verbose_name_plural = 'Residence Syndics'


class residenceAreas(models.Model):
    residence = models.ForeignKey(Residence, null=True, related_name='residence_for_areas', on_delete=models.CASCADE)
    area_name = models.CharField(max_length=140, default='')
    area_prefix = models.CharField(max_length=140, default='')
    area_allotments_from = models.CharField(max_length=140, default='')
    area_allotments_to = models.CharField(max_length=140, default='')
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    code = models.CharField(max_length=120, default='', blank=True, unique=True)
    code_for_app = models.CharField(max_length=120, default='', blank=True, unique=True)
    def __str__(self):
        return self.area_name
    class Meta:
        verbose_name = 'Residence Area'
        verbose_name_plural = 'Residence Areas'
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.code)
        canvas = Image.new('RGB', (320, 320), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.code}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)




class AppUser(models.Model):
    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=120, default='')
    email = models.CharField(max_length=120, default='')
    passcode = models.CharField(max_length=120, default='', unique=True)
    id_passport_number = models.CharField(max_length=120, default='')
    vehicle_number = models.CharField(max_length=120, default='')
    address = models.TextField(max_length=120, default='')
    approved = models.BooleanField(default=True)
    is_child = models.BooleanField(default=False)
    parent_user = models.CharField(max_length=120, default='', null=True, blank=True)
    parent_user_url = models.CharField(max_length=120, default='', null=True, blank=True)
    usertype = models.ForeignKey(appUserTypes, null=True, blank=True, related_name='appusertype', on_delete=models.CASCADE)
    accesstype = models.ForeignKey(visitorAccessTypes, null=True, blank=True, related_name='appuseraccesstype', on_delete=models.CASCADE)
    residence = models.ForeignKey(Residence, null=True, blank=True, related_name='user_residence', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, blank=True, related_name='user_area', on_delete=models.CASCADE)
    login_date = models.DateTimeField(null=True, blank=True)
    logout_date = models.DateTimeField(null=True, blank=True)
    is_logged = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'



class AppUserAssignedAreas(models.Model):
    user = models.ForeignKey(AppUser, null=True, blank=True, related_name='appuser_assigned', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, blank=True, related_name='assigned_user_area', on_delete=models.CASCADE)
    def __str__(self):
        return '***'
    class Meta:
        verbose_name = 'User Assigned Area'
        verbose_name_plural = 'User Assigned Areas'



    







class visitorType(models.Model):
    visitor_type = models.CharField(max_length=120, default='')
    user = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.visitor_type
    class Meta:
        verbose_name = 'Visitor Type'
        verbose_name_plural = 'Visitor Types'

class visitorValidity(models.Model):
    visitor_validity = models.CharField(max_length=120, default='')
    def __str__(self): 
        return self.visitor_validity
    class Meta:
        verbose_name = 'Validity'
        verbose_name_plural = 'Validities'










class Status(models.Model):
    name = models.CharField(max_length=120, default='')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Connection Status'
        verbose_name_plural = 'Connection Statuses'


class Resident(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected")
    )
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default="PENDING")
    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=120, default='')
    email = models.EmailField(max_length=120, default='')
    push_id = models.CharField(max_length=256, default='', null=True)
    id_passport_number = models.CharField(max_length=120, default='')
    vehicle_number = models.CharField(max_length=120, default='')
    block_zone = models.CharField(max_length=120, default='')
    street_name = models.CharField(max_length=120, default='')
    residence_number = models.CharField(max_length=120, default='')
    number_of_resident = models.IntegerField(null=True)
    passcode = models.CharField(max_length=120, default = random.randint(1000,9999), unique=True, blank=True)
    residence_area = models.ForeignKey(residenceAreas, null=True, related_name='residence_area', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'



class Visitor(models.Model):
    name = models.CharField(max_length=120, default='')
    type = models.ForeignKey(visitorType, null=True, related_name='type', on_delete=models.CASCADE)
    timedatefrom = models.DateTimeField(null=True)
    timedateto = models.DateTimeField(null=True)
    registered_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    checkin_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    vehicle_number = models.CharField(max_length=1200, default='')
    number_of_guests = models.IntegerField(default=1)
    resident = models.ForeignKey(Resident, null=True, related_name='visitor_resident', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, related_name='visitor_residence_area', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, related_name='visitor_status', on_delete=models.CASCADE)
    code = models.CharField(max_length=120, default='')
    checkin_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_agent_checkout', on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='visitor_qr_codes', blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = 'Connections'
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.code)
        canvas = Image.new('RGB', (320, 320), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.code}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG') 
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
