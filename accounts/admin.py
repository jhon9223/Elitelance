from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ClientProfile, FreelancerProfile

# remove default registration


class CustomUserAdmin(UserAdmin):

    model = User

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
        ('Profile', {'fields': ('profile_picture',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(ClientProfile)
admin.site.register(FreelancerProfile)
