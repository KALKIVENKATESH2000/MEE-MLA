from django.urls import path
from . import views



urlpatterns = [
    path('admin-register/', views.AdminRegistrationView.as_view(), name='admin-register'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('details/', views.UserDetail.as_view(), name='user-details'),
    path('profile/', views.UserProfileDetail.as_view(), name='create-profile'),
    path('user-mla/', views.UserMLAView.as_view(), name='user-mla-profile'),
]