# -*- encoding: utf-8 -*-
"""
"""

from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files import File
# from PIL import Image, ImageDraw

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


from datetime import datetime
import datetime
from django.utils.timezone import localtime
from time import strftime
import re

from datetime import timedelta

from django.utils.timezone import get_fixed_timezone, utc

import uuid 


from django.contrib.auth.hashers import make_password

import random
import pytz




# date_re = re.compile(
#     r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$'
# )

# time_re = re.compile(
#     r'(?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
#     r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
# )

# datetime_re = re.compile(
#     r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})'
#     r'[T ](?P<hour>\d{1,2}):(?P<minute>\d{1,2})'
#     r'(?::(?P<second>\d{1,2})(?:\.(?P<microsecond>\d{1,6})\d{0,6})?)?'
#     r'(?P<tzinfo>Z|[+-]\d{2}(?::?\d{2})?)?$'
# )

# standard_duration_re = re.compile(
#     r'^'
#     r'(?:(?P<days>-?\d+) (days?, )?)?'
#     r'((?:(?P<hours>-?\d+):)(?=\d+:\d+))?'
#     r'(?:(?P<minutes>-?\d+):)?'
#     r'(?P<seconds>-?\d+)'
#     r'(?:\.(?P<microseconds>\d{1,6})\d{0,6})?'
#     r'$'
# )

# # Support the sections of ISO 8601 date representation that are accepted by
# # timedelta
# iso8601_duration_re = re.compile(
#     r'^(?P<sign>[-+]?)'
#     r'P'
#     r'(?:(?P<days>\d+(.\d+)?)D)?'
#     r'(?:T'
#     r'(?:(?P<hours>\d+(.\d+)?)H)?'
#     r'(?:(?P<minutes>\d+(.\d+)?)M)?'
#     r'(?:(?P<seconds>\d+(.\d+)?)S)?'
#     r')?'
#     r'$'
# )

# # Support PostgreSQL's day-time interval format, e.g. "3 days 04:05:06". The
# # year-month and mixed intervals cannot be converted to a timedelta and thus
# # aren't accepted.
# postgres_interval_re = re.compile(
#     r'^'
#     r'(?:(?P<days>-?\d+) (days? ?))?'
#     r'(?:(?P<sign>[-+])?'
#     r'(?P<hours>\d+):'
#     r'(?P<minutes>\d\d):'
#     r'(?P<seconds>\d\d)'
#     r'(?:\.(?P<microseconds>\d{1,6}))?'
#     r')?$'
# )


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
    can_view_agents = models.BooleanField(default=False)
    can_edit_agents = models.BooleanField(default=False)
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
    address = models.TextField(max_length=1200, default='')
    contact_person = models.CharField(max_length=140, default='')
    contact_email = models.CharField(max_length=140, default='')
    contact_phone = models.CharField(max_length=140, default='')
    company = models.CharField(max_length=140, default='', null=True, blank=True)
    floor = models.CharField(max_length=140, default='', null=True, blank=True)
    type = models.ForeignKey(residenceType, null=True, related_name='residence_type_from', on_delete=models.CASCADE)
    user = models.CharField(max_length=120, default='')
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


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
        canvas = Image.new('RGB', (370, 370), 'white')
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
    vehicle_number = models.CharField(max_length=120, default='', null=True, blank=True)
    address = models.TextField(max_length=1200, default='')
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
    isPermanent = models.BooleanField(default=False)
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
    isActive = models.BooleanField(default=True)
    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=120, default='')
    email = models.EmailField(max_length=120, default='')
    address = models.TextField(max_length=1200, default='')
    push_id = models.CharField(max_length=256, default='', null=True)
    id_passport_number = models.CharField(max_length=120, default='')
    vehicle_number = models.CharField(max_length=120, default='', null=True, blank=True)
    block_zone = models.CharField(max_length=120, default='', null=True, blank=True)
    street_name = models.CharField(max_length=120, default='', null=True, blank=True)
    residence_number = models.CharField(max_length=120, default='', null=True, blank=True)
    number_of_resident = models.IntegerField(null=True)
    passcode = models.CharField(max_length=120, default = random.randint(1000,9999), unique=True, blank=True)
    location = models.CharField(max_length=220, default='', null=True, blank=True)
    recurrance_str = models.CharField(max_length=220, default='', null=True, blank=True)
    time_from = models.DateTimeField(null=True, blank=True)
    time_to = models.DateTimeField(null=True, blank=True)
    residence_area = models.ForeignKey(residenceAreas, null=True, blank=True, related_name='residence_area', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Resident'
        verbose_name_plural = 'Residents'



class Visitor(models.Model):
    name = models.CharField(max_length=120, default='')
    phone = models.CharField(max_length=120, default='', null=True, blank=True)
    email = models.CharField(max_length=120, default='', null=True, blank=True)
    company = models.CharField(max_length=120, default='', null=True, blank=True)
    comment = models.TextField(max_length=1200, default='', null=True, blank=True)
    validity_description = models.CharField(max_length=120, default='', null=True, blank=True)
    type = models.ForeignKey(visitorType, null=True, related_name='type', on_delete=models.CASCADE)
    timedatefrom = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles',default= '/profiles/profile-placeholder.png', null=True, blank=True)
    timedateto = models.DateTimeField(null=True, blank=True)
    overrides_note = models.TextField(max_length=1200, default='',null=True, blank=True)
    registered_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    checkin_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    override = models.BooleanField(default=False)
    vehicle_number = models.CharField(max_length=1200, default='')
    number_of_guests = models.IntegerField(default=1)
    resident = models.ForeignKey(Resident, null=True, blank=True, related_name='visitor_agent_checkin', on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, null=True, blank=True, related_name='user_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_resident', on_delete=models.CASCADE)
    residence_area = models.ForeignKey(residenceAreas, null=True, related_name='visitor_residence_area', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, related_name='visitor_status', on_delete=models.CASCADE)
    code = models.CharField(max_length=120, default='')
    checkin_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='visitor_agent_checkout', on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='visitor_qr_codes', blank=True)
    qr_code_share = models.ImageField(upload_to='visitor_qr_codes', blank=True)
    isPermanent   = models.BooleanField(default=False)
    isEnable      = models.BooleanField(default=True)
    recurrance_str = models.CharField(max_length=220, default='', null=True, blank=True)
    time_from     = models.DateTimeField(null=True, blank=True)
    time_to       = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural = 'Connections'
        
        
    # def parse_datetime(value):
    #     print(value)
    #     """Parse a string and return a datetime.datetime.
    
    #     This function supports time zone offsets. When the input contains one,
    #     the output uses a timezone with a fixed offset from UTC.
    
    #     Raise ValueError if the input is well formatted but not a valid datetime.
    #     Return None if the input isn't well formatted.
    #     """
    #     match = datetime_re.match(value)
    #     if match:
    #         kw = match.groupdict()
    #         kw['microsecond'] = kw['microsecond'] and kw['microsecond'].ljust(6, '0')
    #         tzinfo = kw.pop('tzinfo')
    #         if tzinfo == 'Z':
    #             tzinfo = utc
    #         elif tzinfo is not None:
    #             offset_mins = int(tzinfo[-2:]) if len(tzinfo) > 3 else 0
    #             offset = 60 * int(tzinfo[1:3]) + offset_mins
    #             if tzinfo[0] == '-':
    #                 offset = -offset
    #             tzinfo = get_fixed_timezone(offset)
    #         kw = {k: int(v) for k, v in kw.items() if v is not None}
    #         kw['tzinfo'] = tzinfo
    #         return datetime.datetime(**kw)
        
    def save(self, *args, **kwargs):
        
        qrcode_img = qrcode.make(self.code)
        canvas = Image.new('RGB', (370, 370), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.code}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG') 
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        
        
        
        qrcode_img_share = qrcode.make(self.code)
        canvas_share = Image.new('RGB', (380, 600), 'white')
        draw_share = ImageDraw.Draw(canvas_share)
        canvas_share.paste(qrcode_img_share)
        
        font = ImageFont.load_default()
        # use a bitmap font
        #font = ImageFont.truetype("arial.ttf", 14)
        
        

        spacing = 10
        text = 'Residence / area: ' + self.residence_area.area_name
        
        if not self.user :
            text += '\nResident name: ' + self.resident.name
            text += '\nResident phone: ' + self.resident.phone
            text += '\nResident email: ' + self.resident.email
        if not self.resident :
            text += '\nResident name: ' + self.user.name
            text += '\nResident phone: ' + self.user.phone
            text += '\nResident email: ' + self.user.email
        
        
        
        
        text += '\nVisitor name: ' + self.name
        text += '\nVisitor email: ' + self.email
        text += '\nVisitor phone: ' + self.phone
        text += '\nVisitor vehicle /s number: ' + self.vehicle_number
        if self.timedatefrom :
            text += '\nDate from: ' + str((self.timedatefrom).strftime('%d/%m/%Y %H:%M'))
        if self.timedateto:
            text += '\nDate to: ' + str((self.timedateto).strftime('%d/%m/%Y %H:%M'))
        
        
        # text += '\nDate from: ' + str((self.timedatefrom - timedelta(minutes=10)).strftime('%d %Y %H:%m'))
        # text += '\nDate to: ' + str((self.timedateto - timedelta(minutes=10)).strftime('%d %Y %H:%m'))
          
        # drawing text size 
        draw_share.text((30, 350), text, fill ="black", font = font,  
                  spacing = spacing, align ="left")
        
        fname_share = f'qr_code_share-{self.code}'+'.png'
        buffer = BytesIO()
        canvas_share.save(buffer, 'PNG') 
        
        self.qr_code_share.save(fname_share, File(buffer), save=False)
        canvas_share.close()

        super().save(*args, **kwargs)





 

class Inouts(models.Model):
    inoutpass = models.ForeignKey(Visitor, null=True, related_name='inouts_status', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, null=True, related_name='inouts_status', on_delete=models.CASCADE)
    checkin_date = models.DateTimeField(null=True, blank=True)
    checkout_date = models.DateTimeField(null=True, blank=True)
    checkin_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='inouts_agent_checkin', on_delete=models.CASCADE)
    checkout_agent = models.ForeignKey(AppUser, null=True, blank=True, related_name='inouts_agent_checkout', on_delete=models.CASCADE)
    override = models.BooleanField(default=False)

    def __str__(self):
        return '-'
    class Meta:
        verbose_name = 'Inout'
        verbose_name_plural = 'Inouts'