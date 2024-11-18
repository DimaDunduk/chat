from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django.urls import path
from . import consumers
from chat.consumers import chat_connect, chat_disconnect, chat_receive, loadhistory_connect, loadhistory_disconnect, loadhistory_receive

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]

chat_routing = [
    re_path("websocket.connect", chat_connect),
    re_path("websocket.receive", chat_receive),
    re_path("websocket.disconnect", chat_disconnect)
]
 
loadhistory_routing = [
    re_path("websocket.connect", loadhistory_connect),
    re_path("websocket.receive", loadhistory_receive),
    re_path("websocket.disconnect", loadhistory_disconnect)
]
 
application = ProtocolTypeRouter({
    "websocket": URLRouter(
        chat_routing + loadhistory_routing
    ),
})
    #include(chat_routing, path=r"^/ws/$"),
    #include(loadhistory_routing, path=r"^/loadhistory/$"),
