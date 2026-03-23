from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


# 🔁 CENTRAL ROLE REDIRECT FUNCTION
def redirect_user_by_role(user):

    if user.is_superuser:
        return redirect('/admin/')

    if user.role == 'manager':
        return redirect('manager_dashboard')

    elif user.role == 'client':
        return redirect('client_dashboard')

    elif user.role == 'freelancer':
        return redirect('freelancer_dashboard')

    return redirect('landing_page')


# 🔐 REGISTER
def register_view(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)
            messages.success(request, "Account created successfully!")

            return redirect_user_by_role(user)

        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


# 🔐 LOGIN
def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")

                return redirect_user_by_role(user)

            else:
                messages.error(request, "Invalid username or password")

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


# 🔓 LOGOUT
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('landing_page')


# 👤 PROFILE VIEW
@login_required
def profile_view(request):

    user = request.user  # get the logged in user
    profile = None
    profile_incomplete = False

    if user.role == 'client':
        profile = user.client_profile  # access the related ClientProfile
        # reverse look up

        if not profile.company_name:
            profile_incomplete = True

    elif user.role == 'freelancer':
        profile = user.freelancer_profile

        if not profile.skills or not profile.bio:
            profile_incomplete = True

    # check profile picture also
    if not user.profile_picture:
        profile_incomplete = True

    context = {
        'user': user,
        'profile': profile,
        'profile_incomplete': profile_incomplete,
    }

    return render(request, 'accounts/profile.html', context)


# ✏️ EDIT PROFILE
@login_required
def edit_profile(request):

    user = request.user

    profile = None

    if user.role == 'client':
        profile = user.client_profile
    elif user.role == 'freelancer':
        profile = user.freelancer_profile

    if request.method == 'POST':

        # ✅ PROFILE IMAGE (IMPORTANT)
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')
            user.save()

        # CLIENT
        if user.role == 'client':
            profile.company_name = request.POST.get('company_name')
            profile.company_description = request.POST.get(
                'company_description')
            profile.save()

        # FREELANCER
        elif user.role == 'freelancer':
            profile.skills = request.POST.get('skills')
            profile.bio = request.POST.get('bio')
            profile.hourly_rate = request.POST.get('hourly_rate') or None
            profile.experience = request.POST.get('experience') or None
            profile.portfolio_link = request.POST.get('portfolio_link')
            profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect('profile')

    return render(request, 'accounts/edit_profile.html', {
        'profile': profile
    })


User = get_user_model()


def public_profile_view(request, pk):

    user_obj = get_object_or_404(User, pk=pk)

    profile = None

    if user_obj.role == 'client':
        profile = getattr(user_obj, 'client_profile', None)

    elif user_obj.role == 'freelancer':
        profile = getattr(user_obj, 'freelancer_profile', None)

    context = {
        'profile_user': user_obj,   # 👈 IMPORTANT (not request.user)
        'profile': profile,
    }

    return render(request, 'accounts/public_profile.html', context)
