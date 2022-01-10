from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from realtime.consumers import Consumer
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter([
            path("RT/Cons/", Consumer.as_asgi()),
        ]),
    ),
})
"""
from django.urls import path
from asTest.consumers import Consumer     
ws_urlpatterns = [
   path('asTest/RT/', Consumer.as_asgi())
]
"""

