from django.urls import path
from .consumers import *

ws_urlpatterns = [
    path('ws/book/', BookSocket.as_asgi()),
    path('ws/chatting/', ChattingSocket.as_asgi()),
    path('ws/booking/', BookingSocket.as_asgi()),
    path('ws/chatting/<str:room_name>/', ChatingSocket.as_asgi())
]
