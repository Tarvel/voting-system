from django.contrib.admin.utils import lookup_field
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from base.models import Position, Candidate, Vote, User
from .serializers import (
    PositionSerializer,
    CandidateSerializer,
    VoteSerializer,
    VotingSerializer,
    UserSerializer
)


class PositionListView(generics.ListAPIView):
    """
    API endpoint to list all positions with their candidates
    """
    queryset = Position.objects.prefetch_related('candidates').all()
    serializer_class = PositionSerializer


class PositionDetailView(generics.RetrieveAPIView):
    """
    API endpoint to get details of a specific position
    """
    queryset = Position.objects.prefetch_related('candidates').all()
    serializer_class = PositionSerializer


class CandidateListView(generics.ListAPIView):
    """
    API endpoint to list all candidates
    """
    queryset = Candidate.objects.select_related('position').all()
    serializer_class = CandidateSerializer


class CandidateDetailView(generics.RetrieveAPIView):
    """
    API endpoint to get details of a specific candidate
    """
    queryset = Candidate.objects.select_related('position').all()
    serializer_class = CandidateSerializer


class VoteListView(generics.ListAPIView):
    """
    API endpoint to list user's votes (authenticated users only)
    """
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(user=self.request.user).select_related(
            'candidate', 'position'
        )


class SubmitVoteView(APIView):
    """
    API endpoint to submit votes for all positions at once
    Requires authentication
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VotingSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    created_votes = serializer.save()
                    
                    return Response({
                        'status': 'success',
                        'message': 'Your votes have been submitted successfully',
                        'votes_count': len(created_votes)
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                return Response({
                    'status': 'error',
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    API endpoint to get current staff's profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VotingStatusView(APIView):
    """
    API endpoint to check if staff has already voted
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'has_voted': request.user.has_voted,
            'username': request.user.username
        })
