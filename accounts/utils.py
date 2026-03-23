def is_profile_complete(user):

    if user.role == 'client':
        profile = user.client_profile
        return bool(profile.company_name)

    elif user.role == 'freelancer':
        profile = user.freelancer_profile
        return bool(profile.skills and profile.bio)

    return True
