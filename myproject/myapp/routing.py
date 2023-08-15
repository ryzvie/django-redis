from django.urls import path, re_path
from . import consumers

ws_urlpatterns = [
    path('ws/get_greeting_ws/', consumers.getGreetingWs.as_asgi()),
    path('ws/senddata/', consumers.SendData.as_asgi()),
    path('ws/bg_process/', consumers.BackgroundProcess.as_asgi()),
]