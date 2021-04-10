from django.urls import path
from .consumers import *

ws_urlpatterns = [
    path('ws/book/', BookSocket.as_asgi()),
    path('ws/chat/<str:room_name>', ChatConsumer.as_asgi()),
]
