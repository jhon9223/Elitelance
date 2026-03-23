from django.db import models
from django.conf import settings


class Job(models.Model):

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Proposal(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='proposals'
    )

    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='proposals'
    )

    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cover_letter = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"


class Contract(models.Model):

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
    )

    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )

    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name='contract'
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_contracts'
    )

    freelancer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='freelancer_contracts'
    )

    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    def __str__(self):
        return f"Contract - {self.job.title}"


class Message(models.Model):

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.receiver}"
