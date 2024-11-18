from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from chat.models import ChatMessage, ChatRoom, PetsPerson, PetProfile

def setup_pets_person(request):
    """
    Create a PetsPerson instance for a user if it doesn't already exist.
    """
    # Get the first user (or any user you need)
    user = User.objects.first()  # Modify this to fetch the user you need

    # Check if PetsPerson exists and create if necessary
    pets_person, created = PetsPerson.objects.get_or_create(
        user=user,
        defaults={"city": "Unknown City"}
    )
    message = f"PetsPerson {'created' if created else 'already exists'} for user {user.username}"

    return render(request, 'setup_complete.html', {'message': message})

def user_profile_view(request, user_id):
    """
    View to display a user's profile with their associated pet profile.
    """
    # Get the PetsPerson object or 404 if not found
    pets_person = get_object_or_404(PetsPerson, user_id=user_id)

    # Use the pet_profile property, or default values if not defined
    pet_profile = pets_person.pet_profile

    # Pass data to the template
    return render(request, 'profile.html', {
        'pets_person': pets_person,
        'pet_profile': pet_profile,
    })

@login_required
def chatroom_view(request, room_name):
    """
    View to display a chatroom and handle messages within it.
    """
    # Get the chatroom and PetsPerson for the current user
    chatroom = get_object_or_404(ChatRoom, name=room_name)
    pets_person = get_object_or_404(PetsPerson, user=request.user)

    # Fetch chat messages and active users
    chat_messages = chatroom.messages.order_by('timestamp')
    users_in_chatroom = PetsPerson.objects.filter(user__is_active=True)

    # Handle message posting
    if request.method == "POST":
        message_content = request.POST.get('message')
        if message_content:
            ChatMessage.objects.create(
                chatroom=chatroom,
                user=request.user,
                message=message_content,
                message_html=message_content,  # Simplified for now
            )
            return redirect('chatroom', room_name=room_name)

    # Prepare user profiles for display
    users_with_profiles = []
    for person in users_in_chatroom:
        user_profile = {
            'username': person.user.username,
            'city': person.city or "Unknown City",
            'profile_image': person.profile_image.url if person.profile_image else None,
            'pets': person.pets.all()  # Fetch all pets for this PetsPerson
        }
        users_with_profiles.append(user_profile)

    return render(request, 'chat/chatroom.html', {
        'chatroom': chatroom,
        'users_in_chatroom': users_in_chatroom,
        'chat_messages': chat_messages,
        'users_with_profiles': users_with_profiles,
        'pets_person': pets_person,
    })

@login_required
def send_message(request, room_name):
    """
    Handle sending a message in a chatroom.
    """
    chatroom = get_object_or_404(ChatRoom, name=room_name)
    if request.method == "POST":
        message_content = request.POST.get('message')
        if message_content:
            ChatMessage.objects.create(
                chatroom=chatroom,
                user=request.user,
                message=message_content,
                message_html=message_content,
            )
    return redirect('chatroom', room_name=room_name)

def create_chatroom(request):
    """
    View to create a new chatroom.
    """
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            ChatRoom.objects.create(name=room_name)
            return redirect('chatroom_list')
    return render(request, 'chat/create_chatroom.html')

def chatroom_list(request):
    """
    Display a list of chatrooms with search functionality.
    """
    query = request.GET.get('q')
    if query:
        chatrooms = ChatRoom.objects.filter(name__icontains=query)
    else:
        chatrooms = ChatRoom.objects.all()
    return render(request, 'chat/chatroom_list.html', {'chatrooms': chatrooms, 'query': query})

def home(request):
    """
    Simple homepage view.
    """
    return HttpResponse("Hello, Django!")

class IndexView(generic.View):
    """
    Display the latest 10 chat messages.
    """
    def get(self, request):
        chat_queryset = ChatMessage.objects.order_by("-created")[:10]
        chat_messages = reversed(chat_queryset)

        # Calculate the previous message ID for pagination
        first_message_id = chat_queryset[len(chat_queryset)-1].id if chat_queryset else -1
        previous_id = ChatMessage.objects.filter(pk__lt=first_message_id).order_by("-pk").first()
        previous_id = previous_id.id if previous_id else -1

        return render(request, "chat/chatroom.html", {
            'chat_messages': chat_messages,
            'first_message_id': previous_id,
        })
    



