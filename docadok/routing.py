from django.urls import path
from realtime.consumers import Consumer


"""ws_urlpatterns = [path('/RT/Cons/', Consumer.as_asgi())]
"""


from django.urls import path

#from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("RT/Cons/", Consumer.as_asgi()),
        ]),
    ),

})



