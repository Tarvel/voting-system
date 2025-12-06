from rest_framework import serializers
from base.models import Position, Candidate, Vote, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'has_voted']
        read_only_fields = ['id', 'has_voted']


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'party', 'bio', 'position']
        read_only_fields = ['id']


class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Position
        fields = ['id', 'name', 'description', 'max_votes_allowed', 'candidates']
        read_only_fields = ['id']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user', 'candidate', 'position', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

    def validate(self, data):
        """
        Check that user hasn't already voted for this position
        """
        user = self.context['request'].user
        position = data['position']
        
        if Vote.objects.filter(user=user, position=position).exists():
            raise serializers.ValidationError(
                f"You have already voted for {position.name}"
            )
        
        return data


class VotingSerializer(serializers.Serializer):
    """
    Serializer for handling multiple votes at once
    """
    votes = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def validate_votes(self, value):
        """
        Validate that all positions have exactly one vote
        and user hasn't voted before
        """
        user = self.context['request'].user
        
        if user.has_voted:
            raise serializers.ValidationError("You have already voted")
        
        # Extract position IDs and candidate IDs
        position_ids = set()
        for vote_data in value:
            position_id = vote_data.get('position_id')
            candidate_id = vote_data.get('candidate_id')
            
            if not position_id or not candidate_id:
                raise serializers.ValidationError(
                    "Each vote must have position_id and candidate_id"
                )
            
            # Check for duplicate position votes
            if position_id in position_ids:
                raise serializers.ValidationError(
                    f"Cannot vote twice for the same position"
                )
            position_ids.add(position_id)
            
            # Validate candidate belongs to position
            try:
                candidate = Candidate.objects.get(id=candidate_id)
                if candidate.position_id != position_id:
                    raise serializers.ValidationError(
                        f"Candidate {candidate.name} does not belong to the selected position"
                    )
            except Candidate.DoesNotExist:
                raise serializers.ValidationError(
                    f"Candidate with id {candidate_id} does not exist"
                )
        
        return value

    def create(self, validated_data):
        """
        Create votes for all positions
        """
        user = self.context['request'].user
        votes_data = validated_data['votes']
        created_votes = []
        
        for vote_data in votes_data:
            vote = Vote.objects.create(
                user=user,
                position_id=vote_data['position_id'],
                candidate_id=vote_data['candidate_id']
            )
            created_votes.append(vote)
        
        # Mark user as having voted
        user.has_voted = True
        user.save()
        
        return created_votes
