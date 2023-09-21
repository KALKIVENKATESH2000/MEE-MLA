from django.urls import path
from . import views



urlpatterns = [
    path('superadmin-register/', views.SuperAdminRegistrationView.as_view(), name='superadmin-register'),
    path('admin-register/', views.AdminRegistrationView.as_view(), name='admin-register'),
    path('agent-register/', views.AgentRegistrationView.as_view(), name='agent-register'),
    path('voter-register/', views.VoterRegistrationView.as_view(), name='voter-register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('agent/login/', views.AgentLoginView.as_view(), name='agent-login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('details/', views.UserDetail.as_view(), name='user-details'),
    path('profile/', views.UserProfileDetail.as_view(), name='create-profile'),
    path('user-mla/', views.UserMLAView.as_view(), name='user-mla-profile'),
    path('admin/agents/', views.GetAgentsView.as_view(), name='get-admin-agents'),
    path('admins/', views.GetAdminsView.as_view(), name='get-admins'),

]