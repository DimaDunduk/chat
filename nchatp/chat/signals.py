from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from chat.models import PetsPerson, PetProfile

@receiver(post_save, sender=PetsPerson)
def create_pets_person(sender, instance, created, **kwargs):
    if created and not instance.pet_profile:  # Only create a PetsPerson when a new user is created
        PetsPerson.objects.create(user=instance, city="Unknown City")
        # Create a default pet profile if one doesn't exist
        PetProfile.objects.create(pets_person=instance, city="Unknown City")