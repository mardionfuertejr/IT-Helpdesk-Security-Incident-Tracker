from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from . import views
from . import api_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # NIST Incident Response views
    path('submit/', views.submit_ticket, name='submit_ticket'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket_stage, name='update_ticket_stage'),
    
    # Legacy routes mapped under fallback/aliases for safety
    path('tickets/legacy/', views.ticket_list_view, name='tickets'),
    path('tickets/create/', views.ticket_create_view, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('users/', views.users_view, name='users'),
    path('security-logs/', views.security_logs_view, name='security_logs'),
    path('solutions/<slug:slug>/', views.solutions_detail_view, name='solutions_detail'),
    path('api/token/generate/', views.generate_api_token, name='generate_api_token'),

    # JWT API endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/tickets/', api_views.APITicketListView.as_view(), name='api_tickets'),
    path('api/tickets/create/', api_views.APITicketCreateView.as_view(), name='api_tickets_create'),
]
