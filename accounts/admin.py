from .models import ClientProfile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User, ClientProfile, FreelancerProfile


# ✅ CUSTOM USER ADMIN
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


# ✅ CLIENT PROFILE ADMIN


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'company_name', 'preview')

    fields = (
        'user',
        'company_name',
        'company_description',
        'preview',
    )

    readonly_fields = ('preview',)

    # 🔔 PROFILE IMAGE FROM USER MODEL
    def preview(self, obj):
        if obj.user.profile_picture:
            return format_html(
                '<img src="{}" width="60" style="border-radius:50%;" />',
                obj.user.profile_picture.url
            )
        return "No Image"

    preview.short_description = "Profile Picture"

# ✅ FREELANCER PROFILE ADMIN


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'hourly_rate', 'experience', 'preview')

    fields = (
        'user',
        'skills',
        'bio',
        'hourly_rate',
        'experience',
        'portfolio_link',
        'preview',
    )

    readonly_fields = ('preview',)

    # ✅ FIXED PREVIEW (FROM USER MODEL)
    def preview(self, obj):
        if obj.user.profile_picture:
            return format_html(
                '<img src="{}" width="60" style="border-radius:50%;" />',
                obj.user.profile_picture.url
            )
        return "No Image"

    preview.short_description = "Profile Preview"


# ✅ REGISTER USER ADMIN
admin.site.register(User, CustomUserAdmin)
