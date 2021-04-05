# -*- encoding: utf-8 -*-
"""
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.db.models import Prefetch
from django.utils import timezone
import pytz

from rest_framework import viewsets, generics

from app.serializers import *
from app.models import *

from rest_framework import filters
from django.contrib.auth.hashers import make_password

# import requests
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q
from django.db.models import F
import datetime
from django.utils.timezone import now
from dateutil.rrule import rrulestr
from datetime import datetime
from rest_framework.views import APIView

class ResidenceViewSet(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

class ResidenceSyndicsViewSet(viewsets.ModelViewSet):
    queryset = residenceSyndics.objects.all()
    serializer_class = ResidenceSyndicsSerializer

class ResidenceAreasViewSet(viewsets.ModelViewSet):
    queryset = residenceAreas.objects.all()
    serializer_class = ResidenceAreasSerializer

class ResidenceTypeViewSet(viewsets.ModelViewSet):
    queryset = residenceType.objects.all()
    serializer_class = ResidenceTypeSerializer
 

class SearchVisitorStatus(generics.ListCreateAPIView):
    search_fields = ['status__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer


class SearchVisitorByCode(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def get_queryset(self):
        request_code = self.request.query_params.get('search', None)
        someset = Visitor.objects.all().filter(code=request_code)
        return someset



class SyndicsByResidence(viewsets.ModelViewSet):
    queryset = residenceSyndics.objects.all()
    serializer_class = ResidenceSyndicsSerializer 

    def get_queryset(self):
        request_residence = self.request.query_params.get('residence', None)
        someset = residenceSyndics.objects.all().filter(residence=request_residence)
        return someset



class AreasByResidence(viewsets.ModelViewSet):
    queryset = residenceAreas.objects.all()
    serializer_class = ResidenceAreasSerializer

    def get_queryset(self):
        request_residence = self.request.query_params.get('residence', None)
        someset = residenceAreas.objects.all().filter(residence=request_residence)
        return someset


class ResidencesByUser(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer

    def get_queryset(self):
        request_user = self.request.query_params.get('user', None)
        someset = Residence.objects.all().filter(user=request_user)
        return someset


class ConnectionsByArea(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def get_queryset(self):
        request_area = self.request.query_params.get('area', None)
        someset = Visitor.objects.all().filter(residence_area=request_area)
        return someset


class ResidentsByArea(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def get_queryset(self):
        request_area = self.request.query_params.get('area', None)
        someset = Resident.objects.all().filter(residence_area=request_area)
        return someset


class ResidentsByAreaF(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def get_queryset(self):
        request_area = self.request.query_params.get('area', None)
        someset = Resident.objects.all().filter(residence_area=request_area)
        return someset


class ResidentsByCode(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def get_queryset(self):
        request_code = self.request.query_params.get('code', None)
        if request_code:
            someset = Resident.objects.all().filter(passcode=request_code)
        residence_area_code = self.request.query_params.get('area_code', None)
        if residence_area_code:
            someset = someset.filter(location=residence_area_code)
        return someset


class ResidentsByEmail(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def get_queryset(self):
        request_code = self.request.query_params.get('email', None)
        someset = Resident.objects.all().filter(email=request_code)[:1]
        return someset

# class CheckLoginValidity(viewsets.ModelViewSet):
#     queryset = Resident.objects.all()
#     serializer_class = ResidentSerializer

#     def get_queryset(self):
#         push_id = self.request.query_params.get('push_id', None)
#         someset = Resident.objects.all()
#         print(someset)
#         return True


class CheckLoginValidity(APIView):
    def get(self, request):

        push_id = self.request.query_params.get('push_id', None)
        queryset = Resident.objects.all().filter(push_id=push_id).first()
        rule_string = queryset.recurrance_str

        isValid = False
        dtstart = ''
        str_without_dtstart = ''
        rule_string_perameters = rule_string.split(";")

        for pera in rule_string_perameters:
            if pera.split("=")[0] == 'DTSTART':
                dtstart = pera.split("=")[1]
                rule_string_perameters.remove(pera)

        
        if dtstart != '':
            final_rule_string = "DTSTART:" + dtstart + ";\n" + "RRULE:" + ";".join(rule_string_perameters)
            rule = rrulestr(final_rule_string)
            launchTime = datetime.now(tz=timezone.utc)
            next_occurance = rule.after(launchTime, inc=True)
        else:
            final_rule_string =  "RRULE:" + ";".join(rule_string_perameters)
            rule = rrulestr(final_rule_string)
            launchTime = datetime.utcnow()
            next_occurance = rule.after(launchTime, inc=True)

        # print("final_rule_string : " + final_rule_string)
        # print("rule :")
        # print(rule)
        

        # print("next_occurance :")
        # print(next_occurance)

        if next_occurance.strftime("%d/%m/%Y") == datetime.now(tz=timezone.utc).strftime("%d/%m/%Y"):
            if queryset.time_from and queryset.time_to:
                begin_time = datetime.time(queryset.time_from)
                end_time   = datetime.time(queryset.time_to)
                check_time = datetime.utcnow().time()
                if begin_time < end_time:
                    isValid =  check_time >= begin_time and check_time <= end_time
                else: # crosses midnight
                    isValid =  check_time >= begin_time or check_time <= end_time
            else:
                isValid = True

        return Response({'isValid': isValid})


class ResidentsByEmailAndPhone(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def get_queryset(self):
        request_code = self.request.query_params.get('email', None)
        request_phone = self.request.query_params.get('phone', None)
        someset = Resident.objects.all().filter(phone=request_phone, email=request_code)[:1]
        return someset

class SearchResidents(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def get_queryset(self):
        request_query  = self.request.query_params.get('search', None)
        someset = Resident.objects.all().filter(
                                              Q(name__icontains=request_query) 
                                            | Q(phone__icontains=request_query)
                                            | Q(address__icontains=request_query) 
                                            | Q(residence_area__area_name__icontains=request_query) 
                                            | Q(block_zone__icontains=request_query) 
                                            | Q(vehicle_number__icontains=request_query) 
                                            )
        return someset

class AppUserByAssignedArea(viewsets.ModelViewSet):
    queryset = AppUserAssignedAreas.objects.all()
    serializer_class = AppUserAssignedAreasSerializer

    def get_queryset(self):
        request_user = self.request.query_params.get('user', None)
        someset = AppUserAssignedAreas.objects.all().filter(user=request_user)
        return someset



class SearchArea(viewsets.ModelViewSet):
    queryset = residenceAreas.objects.all()
    serializer_class = ResidenceAreasSerializer 

    def get_queryset(self):
        request_query = self.request.query_params.get('query', None)
        someset = residenceAreas.objects.all().filter(area_name__icontains=request_query)
        return someset



class SearchVisitorNewNew(generics.ListCreateAPIView):
    search_fields = ['name', 'resident__name', 'user__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
        
        
        
class SearchVisitorNew(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer 

    def get_queryset(self):
        request_query = self.request.query_params.get('search', None)
        request_area = self.request.query_params.get('area', None)
        someset = Visitor.objects.all().filter(
                                            Q(name__icontains=request_query) 
                                            | Q(resident__name__icontains=request_query)
                                            | Q(phone__icontains=request_query) 
                                            | Q(resident__phone__icontains=request_query)
                                            | Q(resident__address__icontains=request_query) 
                                            | Q(residence_area__area_name__icontains=request_query) 
                                            | Q(resident__residence_area__area_name__icontains=request_query) 
                                            | Q(vehicle_number__icontains=request_query) 
                                            | Q(resident__vehicle_number__icontains=request_query) 
                                            ).filter(residence_area__residence=request_area).filter(Q(status__name='Check out') | Q(status__name='Registered')).filter(resident__status='APPROVED').filter(Q(timedateto__gte = now()) | Q(isPermanent = True))
        return someset
        



class SearchVisitor(generics.ListCreateAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer



class visitorTypeViewSet(viewsets.ModelViewSet):
    queryset = visitorType.objects.all()
    serializer_class = visitorTypeSerializer


class AppUserAssignedAreasViewSet(viewsets.ModelViewSet):
    queryset = AppUserAssignedAreas.objects.all()
    serializer_class = AppUserAssignedAreasSerializer



class visitorAccessTypesViewSet(viewsets.ModelViewSet):
    queryset = visitorAccessTypes.objects.all()
    serializer_class = VisitorAccessTypesSerializer



class AppUserTypesViewSet(viewsets.ModelViewSet):
    queryset = appUserTypes.objects.all()
    serializer_class = AppUserTypesSerializer


class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer



class AppUsersByEmail(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def get_queryset(self):
        request_code = self.request.query_params.get('email', None)
        someset = AppUser.objects.all().filter(email=request_code)[:1]
        return someset



class AppUsersByArea(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer 

    def get_queryset(self):
        request_code = self.request.query_params.get('area', None)
        someset = AppUser.objects.all().filter(residence_area=request_code)
        return someset



class AppUsersByAreaAndType(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

    def get_queryset(self):
        request_area = self.request.query_params.get('area', None)
        request_type = self.request.query_params.get('type', None)
        someset = AppUser.objects.all().filter(residence_area=request_area, usertype=request_type)
        return someset



class LoginAppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    def get_queryset(self):
        appuseremail = self.request.query_params.get('email', -1)
        appuserpasscode = self.request.query_params.get('passcode', -1)
        someset = AppUser.objects.all().filter(email=appuseremail, passcode=appuserpasscode)[:1]
        return someset 


class AppUsersByParent(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    def get_queryset(self):
        parent = self.request.query_params.get('parent', -1)
        usertypefrom = self.request.query_params.get('type', -1)
        someset = AppUser.objects.all().filter(parent_user=parent).exclude(usertype = usertypefrom)
        return someset


class AgentsByParent(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    def get_queryset(self):
        parent = self.request.query_params.get('parent', -1)
        usertypefrom = self.request.query_params.get('type', -1)
        someset = AppUser.objects.all().filter(parent_user=parent, usertype = usertypefrom)
        return someset


class ResidenceByArea(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
    def get_queryset(self):
        parent = self.request.query_params.get('residence', -1)
        someset = Residence.objects.all().filter(residence=parent)
        return someset


class AreaByCode(viewsets.ModelViewSet):
    queryset = residenceAreas.objects.all() 
    serializer_class = ResidenceAreasSerializer
    def get_queryset(self):
        codefor = self.request.query_params.get('code', -1)
        someset = residenceAreas.objects.all().filter(code=codefor)[:1]
        return someset 

class AgentByPasscodeAndArea(viewsets.ModelViewSet):
    queryset = AppUser.objects.all() 
    serializer_class = AppUserSerializer
    def get_queryset(self):
        codefor = self.request.query_params.get('number', -1)
        residencefor = self.request.query_params.get('area', -1)
        someset = AppUser.objects.all().filter(usertype=3, passcode=codefor, residence=residencefor)[:1]
        return someset 



class ResidencesByParent(viewsets.ModelViewSet):
    queryset = Residence.objects.all()
    serializer_class = ResidenceSerializer
    def get_queryset(self):
        parent = self.request.query_params.get('parent', -1)
        someset = Residence.objects.all().filter(user=parent)
        return someset

class UserTypesByParent(viewsets.ModelViewSet):
    queryset = visitorType.objects.all()
    serializer_class = visitorTypeSerializer
    def get_queryset(self):
        parent = self.request.query_params.get('parent', -1)
        someset = visitorType.objects.all().filter(user=parent)
        return someset


class ConnectionRequestsViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    def get_queryset(self):
        request_residence = self.request.query_params.get('residence', None)
        someset = Resident.objects.all().filter(status="PENDING", residence=request_residence)
        return someset


class ConnectionsViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    
    def get_queryset(self):
        request_residence = self.request.query_params.get('residence', None)
        someset = Resident.objects.all().filter(residence=request_residence) 
        return someset
        


class visitorValidityViewSet(viewsets.ModelViewSet):
    queryset = visitorValidity.objects.all()
    serializer_class = visitorValiditySerializer

class VisitorViewSet(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

class VisitorsByResident(viewsets.ModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

    def get_queryset(self):
        push_id = self.request.query_params.get('push_id', None)
        someset = Visitor.objects.filter(resident__push_id__contains=push_id) 
        return someset

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ResidentViewSet(viewsets.ModelViewSet):
    queryset = Resident.objects.all().order_by('-status')
    serializer_class = ResidentSerializer


class InoutsViewSet(viewsets.ModelViewSet):
    queryset = Inouts.objects.all()
    serializer_class = InoutsSerializer

@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'error-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'error-500.html' )
        return HttpResponse(html_template.render(context, request))
 
