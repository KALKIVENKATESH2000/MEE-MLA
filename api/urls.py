from django.urls import path, include



urlpatterns = [
    path('', include('master.urls')),
    path('user12/', include('user.urls')),
    # path('user/', include('user.urls')),
]