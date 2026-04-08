from django.shortcuts import get_object_or_404, redirect
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from .models import Job
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Message
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from accounts.decorators import role_required
from .models import Job, Proposal, Contract
from .forms import JobForm, ProposalForm
from django.contrib import messages
User = get_user_model()


def job_list(request):
    """
    Professional job listing view
    - Role-based visibility
    - Search
    - Status filter
    - Sorting
    - Pagination
    """

    # Base queryset
    jobs = Job.objects.all().select_related('created_by')

    #  Search
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    #  Status filter
    status_filter = request.GET.get('status', '')
    if status_filter:
        jobs = jobs.filter(status=status_filter)

    #  Role-based filtering
    if request.user.is_authenticated:
        if request.user.role == 'client':
            jobs = jobs.filter(created_by=request.user)
        elif request.user.role == 'freelancer':
            jobs = jobs.filter(status='open')
    else:
        jobs = jobs.filter(status='open')

    #  Sorting
    sort_by = request.GET.get('sort', '')

    if sort_by == 'budget':
        jobs = jobs.order_by('-budget')
    elif sort_by == 'deadline':
        jobs = jobs.order_by('deadline')
    else:
        jobs = jobs.order_by('-created_at')

    #  Pagination
    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #  Flags for template (IMPORTANT FIX)
    is_budget = sort_by == 'budget'
    is_deadline = sort_by == 'deadline'

    is_open = status_filter == 'open'
    is_in_progress = status_filter == 'in_progress'
    is_completed = status_filter == 'completed'

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,

        'is_budget': is_budget,
        'is_deadline': is_deadline,

        'is_open': is_open,
        'is_in_progress': is_in_progress,
        'is_completed': is_completed,
    }

    return render(request, 'jobs/job_list.html', context)

# Job Create (Client Only)


@login_required
@role_required('client')
def job_create(request):

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.status = 'open'
            job.save()

            messages.success(request, "Job posted successfully!")
            return redirect('job_list')

        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = JobForm()

    return render(request, 'jobs/job_create.html', {
        'form': form
    })


# Job Detail

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})


# Submit Proposal (Freelancer Only)

@login_required
@role_required('freelancer')
def submit_proposal(request, pk):

    job = get_object_or_404(Job, pk=pk)

    # Job must be open
    if job.status != 'open':
        raise PermissionDenied("Job is not open.")

    # Cannot apply to own job
    if job.created_by == request.user:
        raise PermissionDenied("You cannot apply to your own job.")

    # Prevent duplicate proposals
    if Proposal.objects.filter(job=job, freelancer=request.user).exists():
        raise PermissionDenied("You already applied for this job.")

    if request.method == 'POST':
        form = ProposalForm(request.POST)

        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.job = job
            proposal.freelancer = request.user
            proposal.status = 'pending'
            proposal.save()

            return redirect('job_list')

    else:
        form = ProposalForm()

    return render(request, 'jobs/submit_proposal.html', {
        'form': form,
        'job': job
    })


# View Proposals for a Job (Client Only)

@login_required
@role_required('client')
def job_proposals(request, pk):

    job = get_object_or_404(Job, pk=pk)

    if job.created_by != request.user:
        raise PermissionDenied("You are not allowed to view these proposals.")

    proposals = Proposal.objects.filter(job=job)

    return render(request, 'jobs/job_proposals.html', {
        'job': job,
        'proposals': proposals
    })


# Accept Proposal (Client Only)

@login_required
@role_required('client')
def accept_proposal(request, pk):

    proposal = get_object_or_404(Proposal, pk=pk)
    job = proposal.job

    # Ensure only job owner can accept
    if job.created_by != request.user:
        raise PermissionDenied("You are not allowed to accept this proposal.")

    # Ensure job is still open
    if job.status != 'open':
        raise PermissionDenied("This job is no longer open.")

    # Prevent accepting non-pending proposals
    if proposal.status != 'pending':
        raise PermissionDenied("This proposal cannot be accepted.")

    # Extra safety: prevent duplicate contract
    if Contract.objects.filter(job=job).exists():
        raise PermissionDenied("Contract already exists for this job.")

    # Accept selected proposal
    proposal.status = 'accepted'
    proposal.save()

    # Reject all other proposals
    Proposal.objects.filter(
        job=job
    ).exclude(
        pk=proposal.pk
    ).update(status='rejected')

    # Update job status
    job.status = 'in_progress'
    job.save()

    # Create contract automatically
    Contract.objects.create(
        job=job,
        client=job.created_by,
        freelancer=proposal.freelancer,
        status='active',
        payment_status='pending'
    )

    return redirect('job_proposals', pk=job.pk)


# My Proposals (Freelancer)

@login_required
@role_required('freelancer')
def my_proposals(request):

    proposals = Proposal.objects.filter(
        freelancer=request.user
    ).order_by('-submitted_at')

    return render(request, 'jobs/my_proposals.html', {
        'proposals': proposals
    })


# Contract List

@login_required
def contract_list(request):

    if request.user.role == 'client':
        contracts = Contract.objects.filter(client=request.user)

    elif request.user.role == 'freelancer':
        contracts = Contract.objects.filter(freelancer=request.user)

    else:
        contracts = Contract.objects.all()

    return render(request, 'jobs/contract_list.html', {
        'contracts': contracts
    })


# Complete Job (Client Only)

@login_required
@role_required('client')
def complete_job(request, pk):

    job = get_object_or_404(Job, pk=pk)

    # Only job owner can complete
    if job.created_by != request.user:
        raise PermissionDenied("Not allowed.")

    # Job must be in progress
    if job.status != 'in_progress':
        raise PermissionDenied("Job is not in progress.")

    # Update job status
    job.status = 'completed'
    job.save()

    # Update contract
    contract = Contract.objects.filter(job=job).first()

    if contract:
        contract.status = 'completed'
        contract.payment_status = 'paid'
        contract.save()

    return redirect('job_detail', pk=job.pk)


#  Explore Clients (for freelancers)
def explore_clients(request):

    clients = User.objects.filter(role='client')

    paginator = Paginator(clients, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/explore_clients.html', {
        'page_obj': page_obj
    })


#  Explore Freelancers (for clients)

User = get_user_model()


def explore_freelancers(request):

    freelancers = User.objects.filter(role='freelancer')

    paginator = Paginator(freelancers, 6)  # 6 per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/explore_freelancers.html', {
        'page_obj': page_obj
    })


@login_required
def chat_view(request, user_id):

    other_user = get_object_or_404(User, id=user_id)

    messages = Message.objects.filter(
        sender=request.user,
        receiver=other_user
    ) | Message.objects.filter(
        sender=other_user,
        receiver=request.user
    )

    messages = messages.order_by('timestamp')

    #  Send message
    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

    return render(request, 'jobs/chat.html', {
        'messages': messages,
        'other_user': other_user
    })


@login_required
def inbox_view(request):

    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )

    users = set()

    for msg in messages:
        if msg.sender != request.user:
            users.add(msg.sender)
        if msg.receiver != request.user:
            users.add(msg.receiver)

    return render(request, 'jobs/inbox.html', {
        'users': users
    })


@csrf_exempt
def generate_job_description(request):

    if request.method == "POST":

        data = json.loads(request.body)
        title = data.get("title", "")

        if not title:
            return JsonResponse({"description": "Please enter a title first."})

        prompt = f"""
        Write a professional freelance job description for:

        {title}

        Include:
        - Overview
        - Responsibilities
        - Skills Required
        """

        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

        headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
        }

        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": prompt},
                timeout=20
            )

            result = response.json()
            print("AI RAW:", result)

            if isinstance(result, list) and "generated_text" in result[0]:
                return JsonResponse({
                    "description": result[0]["generated_text"]
                })

        except Exception as e:
            print("AI ERROR:", str(e))

        fallback = f"""
We are looking for a skilled {title} to join our team.

Responsibilities:
- Develop and maintain high-quality solutions
- Collaborate with cross-functional teams
- Deliver projects on time

Required Skills:
- Strong experience in relevant technologies
- Problem-solving ability
- Good communication skills
"""

        return JsonResponse({
            "description": fallback
        })


@csrf_exempt
def generate_proposal(request):

    if request.method == "POST":

        data = json.loads(request.body)
        title = data.get("title", "")

        prompt = f"""
        Write a professional freelance proposal for the job:

        {title}

        Make it:
        - Friendly
        - Confident
        - Short
        """

        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

        headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
        }

        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": prompt},
                timeout=20
            )

            result = response.json()

            if isinstance(result, list) and "generated_text" in result[0]:
                return JsonResponse({
                    "proposal": result[0]["generated_text"]
                })

        except:
            pass

        # fallback
        fallback = f"""
Hi,

I am very interested in your project "{title}".

I have strong experience and can deliver high-quality work within the deadline.

Looking forward to working with you.

Thanks.
"""

        return JsonResponse({
            "proposal": fallback
        })


@login_required
def job_delete(request, pk):

    job = get_object_or_404(Job, pk=pk)

    #  Only owner can delete
    if job.created_by != request.user:
        raise PermissionDenied("You are not allowed to delete this job.")

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect("job_list")

    return redirect("job_list")


@login_required
def delete_proposal(request, pk):

    proposal = get_object_or_404(Proposal, pk=pk)

    # Only owner can delete
    if proposal.freelancer != request.user:
        raise PermissionDenied

    # Only pending proposals
    if proposal.status != "pending":
        messages.error(request, "You cannot delete this proposal.")
        return redirect("my_proposals")

    if request.method == "POST":
        proposal.delete()
        messages.success(request, "Proposal deleted successfully!")

    return redirect("my_proposals")
