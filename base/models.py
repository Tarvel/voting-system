from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model. 
    Inherits fields like username, password, email from AbstractUser.
    """
    has_voted = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    max_votes_allowed = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')

    def __str__(self):
        return f"{self.name} ({self.position.name})"

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'position')

    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"