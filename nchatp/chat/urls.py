from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chatroom_view, name='chatroom'), #chatroom_list instead of chatroom_view!!
    path('chat/<str:room_name>/send/', views.send_message, name='send_message'),
    path('', views.home, name='home'),
    path('chatrooms/', views.chatroom_list, name='chatroom_list'),
    path('chatroom/create/', views.create_chatroom, name='create_chatroom'),
    
]