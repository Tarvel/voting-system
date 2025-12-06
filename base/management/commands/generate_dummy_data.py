from django.core.management.base import BaseCommand
from base.models import Position, Candidate


class Command(BaseCommand):
    help = 'Generate dummy voting data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating dummy voting data...')

        # Clear existing data
        Candidate.objects.all().delete()
        Position.objects.all().delete()

        # Create Positions
        positions_data = [
            {
                'name': 'President',
                'description': 'Lead the organization and represent students',
                'max_votes_allowed': 1
            },
            {
                'name': 'Vice President',
                'description': 'Support the President and oversee committees',
                'max_votes_allowed': 1
            },
            {
                'name': 'Secretary',
                'description': 'Manage records and communications',
                'max_votes_allowed': 1
            },
            {
                'name': 'Treasurer',
                'description': 'Oversee financial matters and budgets',
                'max_votes_allowed': 1
            },
        ]

        positions = []
        for pos_data in positions_data:
            position = Position.objects.create(**pos_data)
            positions.append(position)
            self.stdout.write(self.style.SUCCESS(f'Created position: {position.name}'))

        # Create Candidates for each position
        candidates_data = {
            'President': [
                {'name': 'Sarah Johnson', 'party': 'Progressive Alliance', 'bio': 'Experienced leader with 5 years in student government.'},
                {'name': 'Michael Chen', 'party': 'Unity Party', 'bio': 'Current VP with vision for modernizing campus facilities.'},
                {'name': 'Emma Williams', 'party': 'Independent', 'bio': 'Fresh perspective on student life and diversity initiatives.'},
            ],
            'Vice President': [
                {'name': 'James Rodriguez', 'party': 'Progressive Alliance', 'bio': 'Dedicated team player with experience in event management.'},
                {'name': 'Olivia Martinez', 'party': 'Unity Party', 'bio': 'Strong communicator focused on bridging gaps.'},
                {'name': 'David Kim', 'party': 'Tech Forward', 'bio': 'Technology enthusiast aiming to bring digital innovation.'},
            ],
            'Secretary': [
                {'name': 'Sophia Brown', 'party': 'Unity Party', 'bio': 'Detail-oriented organizer with excellent communication skills.'},
                {'name': 'Lucas Anderson', 'party': 'Independent', 'bio': 'Experienced in documentation and record-keeping.'},
                {'name': 'Ava Thompson', 'party': 'Progressive Alliance', 'bio': 'Skilled writer committed to keeping students informed.'},
            ],
            'Treasurer': [
                {'name': 'Noah Davis', 'party': 'Fiscal Responsibility', 'bio': 'Economics major with strong financial acumen.'},
                {'name': 'Isabella Garcia', 'party': 'Unity Party', 'bio': 'Accounting background with focus on transparency.'},
                {'name': 'Ethan Wilson', 'party': 'Independent', 'bio': 'Business student dedicated to maximizing value.'},
            ],
        }

        for position in positions:
            if position.name in candidates_data:
                for candidate_data in candidates_data[position.name]:
                    candidate = Candidate.objects.create(
                        position=position,
                        **candidate_data
                    )
                    self.stdout.write(self.style.SUCCESS(f'  Created candidate: {candidate.name}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Dummy data generation complete!'))
        self.stdout.write(f'Created {Position.objects.count()} positions')
        self.stdout.write(f'Created {Candidate.objects.count()} candidates')
