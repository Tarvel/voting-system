from django.urls import path
from .views import (
    PositionListView,
    PositionDetailView,
    CandidateListView,
    CandidateDetailView,
    VoteListView,
    SubmitVoteView,
    UserProfileView,
    VotingStatusView
)

app_name = 'api'

urlpatterns = [
    # Position endpoints
    path('positions/', PositionListView.as_view(), name='position-list'),
    path('positions/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    
    # Candidate endpoints
    path('candidates/', CandidateListView.as_view(), name='candidate-list'),
    path('candidates/<int:pk>/', CandidateDetailView.as_view(), name='candidate-detail'),
    
    # Vote endpoints
    path('votes/', VoteListView.as_view(), name='vote-list'),
    path('vote/submit/', SubmitVoteView.as_view(), name='vote-submit'),
    
    # User endpoints
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('user/status/', VotingStatusView.as_view(), name='voting-status'),
]
