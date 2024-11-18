from django.db import migrations
from django.contrib.auth.models import User
from chat.models import PetsPerson

def create_pets_person(apps, schema_editor):
    # Create a PetsPerson object for each user
    for user in User.objects.all():
        if not PetsPerson.objects.filter(user=user).exists():
            PetsPerson.objects.create(user=user, city="Unknown City")

class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_pets_person),
    ]