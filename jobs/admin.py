from .models import Message
from django.contrib import admin
from .models import Job, Proposal, Contract
# Register your models here.

admin.site.register(Proposal)
admin.site.register(Contract)

admin.site.register(Message)
