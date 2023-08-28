from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profile/', views.UserProfileDetail.as_view(), name='create-profile'),
]