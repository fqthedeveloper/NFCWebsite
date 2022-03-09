import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NFCMMAClub.settings')


from channels.routing import ProtocolTypeRouter, URLRouter
import NFCapp.routing
application = get_asgi_application()
application=ProtocolTypeRouter({
	'websocket':URLRouter(NFCapp.routing.ws_patterns)
})
