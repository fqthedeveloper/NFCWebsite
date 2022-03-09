
from django.urls import path
from NFCMMAClub import asgi
from .consumers import NotificationConsumer

ws_patterns=[
	path('ws/notifications/',NotificationConsumer.as_asgi()),
]