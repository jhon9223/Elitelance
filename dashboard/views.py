from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from jobs.models import Job, Proposal, Contract
from accounts.decorators import role_required
from accounts.views import redirect_user_by_role

User = get_user_model()


#  DASHBOARD ROUTER
@login_required
def dashboard_home(request):
    return redirect_user_by_role(request.user)


#  CLIENT DASHBOARD
@login_required
@role_required('client')
def client_dashboard(request):

    user = request.user

    total_jobs = Job.objects.filter(created_by=user).count()
    open_jobs = Job.objects.filter(created_by=user, status='open').count()
    in_progress_jobs = Job.objects.filter(
        created_by=user, status='in_progress').count()
    completed_jobs = Job.objects.filter(
        created_by=user, status='completed').count()

    pending_proposals = Proposal.objects.filter(
        job__created_by=user,
        status='pending'
    ).count()

    recent_jobs = Job.objects.filter(
        created_by=user
    ).order_by('-created_at')[:5]

    recent_proposals = Proposal.objects.filter(
        job__created_by=user
    ).select_related('freelancer', 'job').order_by('-submitted_at')[:5]

    #  NOTIFICATIONS
    notifications = []

    if pending_proposals > 0:
        notifications.append(f"{pending_proposals} new proposals received")

    notification_count = len(notifications)

    context = {
        'total_jobs': total_jobs,
        'open_jobs': open_jobs,
        'in_progress_jobs': in_progress_jobs,
        'completed_jobs': completed_jobs,
        'pending_proposals': pending_proposals,
        'recent_jobs': recent_jobs,
        'recent_proposals': recent_proposals,

        #  notifications
        'notifications': notifications,
        'notification_count': notification_count,
    }

    return render(request, 'dashboard/client_dashboard.html', context)


#  FREELANCER DASHBOARD
@login_required
@role_required('freelancer')
def freelancer_dashboard(request):

    user = request.user

    total_proposals = Proposal.objects.filter(freelancer=user).count()

    accepted_proposals = Proposal.objects.filter(
        freelancer=user,
        status='accepted'
    ).count()

    active_contracts = Contract.objects.filter(
        freelancer=user,
        status='active'
    ).count()

    completed_contracts = Contract.objects.filter(
        freelancer=user,
        status='completed'
    ).count()

    recent_proposals = Proposal.objects.filter(
        freelancer=user
    ).select_related('job').order_by('-submitted_at')[:5]

    recent_contracts = Contract.objects.filter(
        freelancer=user
    ).select_related('job').order_by('-start_date')[:5]

    #  NOTIFICATIONS
    notifications = []

    if accepted_proposals > 0:
        notifications.append(f"{accepted_proposals} proposals accepted 🎉")

    notification_count = len(notifications)

    context = {
        'total_proposals': total_proposals,
        'accepted_proposals': accepted_proposals,
        'active_contracts': active_contracts,
        'completed_contracts': completed_contracts,
        'recent_proposals': recent_proposals,
        'recent_contracts': recent_contracts,

        #  notifications
        'notifications': notifications,
        'notification_count': notification_count,
    }

    return render(request, 'dashboard/freelancer_dashboard.html', context)


#  MANAGER DASHBOARD
@login_required
@role_required('manager')
def manager_dashboard(request):

    total_users = User.objects.count()
    total_jobs = Job.objects.count()
    total_proposals = Proposal.objects.count()
    total_contracts = Contract.objects.count()

    open_jobs = Job.objects.filter(status='open').count()
    in_progress_jobs = Job.objects.filter(status='in_progress').count()
    completed_jobs = Job.objects.filter(status='completed').count()

    recent_jobs = Job.objects.select_related(
        'created_by').order_by('-created_at')[:5]

    recent_contracts = Contract.objects.select_related(
        'client', 'freelancer', 'job'
    ).order_by('-start_date')[:5]

    #  NOTIFICATIONS
    notifications = []

    if total_jobs > 0:
        notifications.append(f"{total_jobs} total jobs on platform")

    notification_count = len(notifications)

    context = {
        'total_users': total_users,
        'total_jobs': total_jobs,
        'total_proposals': total_proposals,
        'total_contracts': total_contracts,
        'open_jobs': open_jobs,
        'in_progress_jobs': in_progress_jobs,
        'completed_jobs': completed_jobs,
        'recent_jobs': recent_jobs,
        'recent_contracts': recent_contracts,

        #  notifications
        'notifications': notifications,
        'notification_count': notification_count,
    }

    return render(request, 'dashboard/manager_dashboard.html', context)
