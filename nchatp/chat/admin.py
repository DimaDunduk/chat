from django.contrib import admin
from .models import ChatRoom, ChatMessage
from .models import PetsPerson

admin.site.register(ChatRoom)
admin.site.register(ChatMessage)
admin.site.register(PetsPerson)

# Register your models here.
