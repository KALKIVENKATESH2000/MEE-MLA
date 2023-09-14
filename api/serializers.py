from rest_framework import serializers 
from .models import Constituency, District, State, PollingStation


class ConstituencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Constituency
        fields = "__all__"
        
        
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"
        
        
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"
        
class PollingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollingStation
        fields = "__all__"