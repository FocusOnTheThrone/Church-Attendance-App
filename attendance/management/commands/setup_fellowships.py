from django.core.management.base import BaseCommand
from attendance.models import Fellowship


class Command(BaseCommand):
    help = 'Set up default fellowships for the church management system'

    def handle(self, *args, **options):
        """Create default fellowships if they don't exist."""
        
        default_fellowships = [
            {
                "name": "Men's Fellowship",
                "description": "Fellowship group for men in the church"
            },
            {
                "name": "Women's Fellowship", 
                "description": "Fellowship group for women in the church"
            },
            {
                "name": "Youth Fellowship",
                "description": "Fellowship group for young adults and teenagers"
            },
            {
                "name": "Children",
                "description": "Children's ministry and fellowship activities"
            },
            {
                "name": "Choir",
                "description": "Church choir and music ministry"
            },
            {
                "name": "Ushering",
                "description": "Ushering and hospitality ministry"
            },
            {
                "name": "Prayer",
                "description": "Prayer team and intercessory ministry"
            },
            {
                "name": "None",
                "description": "No specific fellowship group"
            },
            {
                "name": "Other",
                "description": "Other fellowship groups not listed above"
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for fellowship_data in default_fellowships:
            fellowship, created = Fellowship.objects.update_or_create(
                name=fellowship_data["name"],
                defaults={
                    "description": fellowship_data["description"],
                    "is_active": True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created fellowship: {fellowship.name}')
                )
            else:
                # Update description if it exists
                fellowship.description = fellowship_data["description"]
                fellowship.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated fellowship: {fellowship.name}')
                )
        
        total_fellowships = Fellowship.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nFellowship setup complete!\n'
                f'Created: {created_count} new fellowships\n'
                f'Updated: {updated_count} existing fellowships\n'
                f'Total fellowships in database: {total_fellowships}'
            )
        )
