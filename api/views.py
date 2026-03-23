from rest_framework.decorators import api_view, permission_classes
from .serializers import ProposalSerializer
from jobs.models import Proposal
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from jobs.models import Job
from .serializers import JobSerializer


@api_view(['GET'])
def job_list_api(request):

    jobs = Job.objects.filter(status='open')
    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def proposal_list_api(request):

    proposals = Proposal.objects.filter(freelancer=request.user)
    serializer = ProposalSerializer(proposals, many=True)

    return Response(serializer.data)
