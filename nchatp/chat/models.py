from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PetsPerson(models.Model):
    """
    Model representing a person associated with pets.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='petsperson')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/profile_images/', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PetProfile(models.Model):
    """
    Model representing the profile of a pet.
    """
    owner = models.OneToOneField(PetsPerson, on_delete=models.CASCADE, related_name='pet_profile')
    name = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    chip_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pet Profile: {self.name or 'Unnamed'}"


class Pet(models.Model):
    """
    Model representing individual pets.
    """
    name = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    chip_id = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(PetsPerson, on_delete=models.CASCADE, related_name='pets', blank=True, null=True)
    image = models.ImageField(upload_to='pet_images/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('pet_detail', kwargs={"pk": self.pk})

    def __str__(self):
        return self.name or 'Unnamed'


class ChatRoom(models.Model):
    """
    Model representing chat rooms.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    """
    Model representing chat messages in a room.
    """
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=3000)
    message_html = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}: {self.message[:50]} ({self.timestamp})"


class City(models.Model):
    """
    Model representing a city.
    """
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_de = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_en or self.name_de