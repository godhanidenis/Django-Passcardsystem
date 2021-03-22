from rest_framework import serializers
from app.models import Residence, visitorType, visitorValidity, Visitor, Resident, Status, residenceType, visitorAccessTypes, appUserTypes, AppUser, residenceSyndics, residenceAreas, AppUserAssignedAreas, Inouts
# , QRCode


class ResidenceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = residenceType
        fields = '__all__'

class ResidenceSyndicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = residenceSyndics
        fields = '__all__'

class ResidenceAreasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = residenceAreas
        fields = '__all__'

# class VisitorSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Visitor
#         fields = '__all__'


class ResidenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Residence
        fields = '__all__'

class visitorTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = visitorType
        fields = '__all__'

class visitorValiditySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = visitorValidity
        fields = '__all__'

class visitorValiditySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = visitorValidity
        fields = '__all__'

class VisitorAccessTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = visitorAccessTypes
        fields = '__all__'

class ResidentSerializer(serializers.HyperlinkedModelSerializer):
    res_area = ResidenceAreasSerializer(source='residence_area', read_only=True)
   
    class Meta:
        model = Resident
        fields = '__all__'
        extra_fields = ['url']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ResidentSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class StatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class AppUserTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = appUserTypes
        fields = '__all__'

class AppUserSerializer(serializers.HyperlinkedModelSerializer):
    res_area = ResidenceAreasSerializer(source='residence_area', read_only=True)
    res_type = AppUserTypesSerializer(source='usertype', read_only=True)
   
    class Meta:
        model = AppUser
        fields = '__all__'
        extra_fields = ['url']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(AppUserSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class AppUserAssignedAreasSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUserAssignedAreas
        fields = '__all__'
        
        
class VisitorSerializer(serializers.HyperlinkedModelSerializer):
    visitor_area = ResidenceAreasSerializer(source='residence_area', read_only=True)
    visitor_resident = ResidentSerializer(source='resident', read_only=True)
    visitor_user = AppUserSerializer(source='user', read_only=True)
    visitor_type = visitorTypeSerializer(source='type', read_only=True)
    visitor_status = StatusSerializer(source='status', read_only=True)
    
    class Meta:
        model = Visitor
        fields = '__all__'
        extra_fields = ['url']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(VisitorSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields



class InoutsSerializer(serializers.HyperlinkedModelSerializer):
    inout_pass = VisitorSerializer(source='inoutpass', read_only=True)
    inout_status = StatusSerializer(source='status', read_only=True)
    inout_checkin_agent = AppUserSerializer(source='checkin_agent', read_only=True)
    inout_checkout_agent = AppUserSerializer(source='checkout_agent', read_only=True)
    
    class Meta:
        model = Inouts
        fields = '__all__'
        extra_fields = ['url']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(InoutsSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
