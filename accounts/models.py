from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )


class ClientProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_profile'
    )

    company_name = models.CharField(max_length=255, blank=True)
    company_description = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class FreelancerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='freelancer_profile'
    )

    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    experience = models.PositiveIntegerField(null=True, blank=True)
    portfolio_link = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
