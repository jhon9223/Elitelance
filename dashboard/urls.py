from django.urls import path
from . import views

urlpatterns = [

    # Dashboard router
    path('', views.dashboard_home, name='dashboard_home'),

    # Role dashboards
    path('client/', views.client_dashboard, name='client_dashboard'),
    path('freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),

]
