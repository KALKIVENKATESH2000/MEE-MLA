from django.urls import path, include
from .views import *


urlpatterns = [
    path('', include('master.urls')),
    path('user/', include('user.urls')),
    path('constituency/', ConstituencyListCreate.as_view(), name='constituency-list-create'),
    path('polling_stations/', PollingStationListCreate.as_view(), name='polling_stations-list-create'),
    path('polling_stations/<int:pk>/', PollingStationsByConstituency.as_view(), name='polling-stations-by-constituency'),
    path('polling_stations/<int:pk>/voters/', VotersByPollingStation.as_view(), name='voters-by-polling-station'),
    path('admin/polling-stations/', PollingStationsInView.as_view(), name='admin-polling-stations'),
    path('agent/voters/', AgentVotersByPollingStation.as_view(), name='agent-voters'),
]