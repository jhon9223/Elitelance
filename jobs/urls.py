from django.urls import path
from . import views

urlpatterns = [

    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/proposals/', views.job_proposals, name='job_proposals'),
    path('<int:pk>/apply/', views.submit_proposal, name='submit_proposal'),
    path('proposal/<int:pk>/accept/',
         views.accept_proposal, name='accept_proposal'),
    path('my-proposals/', views.my_proposals, name='my_proposals'),
    path('contracts/', views.contract_list, name='contract_list'),
    path('<int:pk>/complete/', views.complete_job, name='complete_job'),
    path('explore/clients/', views.explore_clients, name='explore_clients'),
    path('explore/freelancers/', views.explore_freelancers,
         name='explore_freelancers'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
    path('messages/', views.inbox_view, name='inbox'),
    path('ai/generate-job-description/',
         views.generate_job_description, name='ai_job'),
    path('ai/generate-proposal/', views.generate_proposal, name='ai_proposal'),
    path('delete/<int:pk>/', views.job_delete, name='job_delete'),
    path('proposal/delete/<int:pk>/',
         views.delete_proposal, name='delete_proposal'),
]
