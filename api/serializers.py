
from rest_framework import serializers
from jobs.models import Job, Proposal


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description',
                  'budget', 'status', 'created_at']


class ProposalSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)

    class Meta:
        model = Proposal
        fields = ['id', 'job', 'job_title',
                  'bid_amount', 'status', 'submitted_at']
