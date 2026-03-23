from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list_api),
    path('proposals/', views.proposal_list_api, name='api_proposals'),
]
