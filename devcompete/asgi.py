import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devcompete.settings')
django.setup()
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import contest.routing

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            contest.routing.websocket_urlpatterns
        )
    ),
    'http': django_asgi_app,
})
