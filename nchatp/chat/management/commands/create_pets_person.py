# chat/management/commands/create_pets_person.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from chat.models import PetsPerson

class Command(BaseCommand):
    help = 'Creates a PetsPerson for an existing user'

    def handle(self, *args, **kwargs):
        # Replace with the desired user (or use a filter to select a user)
        user = User.objects.first()  # You can adjust the query here
        
        # Check if the user already has a PetsPerson
        if not PetsPerson.objects.filter(user=user).exists():
            PetsPerson.objects.create(user=user, city="Unknown City")
            self.stdout.write(self.style.SUCCESS(f'PetsPerson created for user {user.username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'PetsPerson already exists for user {user.username}'))