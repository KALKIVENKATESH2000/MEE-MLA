from django.shortcuts import render
from rest_framework import generics
from django.http.response import JsonResponse
from rest_framework.response import Response
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from .models import Constituency, State, District, PollingStation
from .serializers import ConstituencySerializer, PollingStationSerializer
from rest_framework.permissions import IsAuthenticated
from master.models import Voter
from master.serializers import VoterSerializer

# Create your views here.

def is_admin(user):
    return user.is_authenticated and user.roles == 'admin'


# @user_passes_test(is_admin)
class PollingStationsInView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        admin_user = request.user
        constituency = admin_user.constituency
        if constituency:
            polling_stations = PollingStation.objects.filter(constituency=constituency)
            polling_stations_data = [{'id': station.id,'no': station.no, 'name': station.name, 'location': station.location} for station in polling_stations]
            return JsonResponse({'constituency': constituency.name, 'polling_stations': polling_stations_data})
        else:
            return JsonResponse({'error': 'Admin user is not assigned to a constituency'}, status=400)

class AgentVotersByPollingStation(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agent_user = request.user
        polling_station = agent_user.polling_station
        constituency = agent_user.constituency.name
        if polling_station:
            voters = Voter.objects.filter(polling_station=polling_station)
            voters_count = voters.count()
            # voters_data = [{'id': voter.id,'name': voter.name, 'surname': voter.surname, 'address': voter.address} for voter in voters]
            serializer = VoterSerializer(voters, many=True)
            return JsonResponse({'constituency':constituency, 'polling_station': polling_station.name, 'locations':polling_station.location,'voters':voters_count, 'voters_data': serializer.data})
        else:
            return JsonResponse({'error': 'Admin user is not assigned to a polling station'}, status=400)


class ConstituencyListCreate(generics.ListCreateAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer

    
class PollingStationListCreate(generics.ListCreateAPIView):
    queryset = PollingStation.objects.all()
    serializer_class = PollingStationSerializer
    
    
class PollingStationsByConstituency(generics.ListAPIView):
    serializer_class = PollingStationSerializer

    def get_queryset(self):
        # constituency_id = self.request.query_params.get('constituency_id')
        constituency_id = self.kwargs['pk']

        return PollingStation.objects.filter(constituency_id=constituency_id)
    
class VotersByPollingStation(generics.ListAPIView):
    serializer_class = VoterSerializer

    def get_queryset(self):
        # constituency_id = self.request.query_params.get('constituency_id')
        polling_station = self.kwargs['pk']

        return Voter.objects.filter(polling_station=polling_station)
    
class AgentVoter(generics.ListAPIView):
    serializer_class = VoterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        agent = self.request.user.polling_station
        print(agent)
        return Voter.objects.filter(polling_station=agent)