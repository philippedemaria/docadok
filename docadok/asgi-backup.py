"""
ASGI config for docado project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/

"""
import os
import django
from channels.routing import get_default_application
#from django.core.asgi import get_asgi_application
#from channels.auth import AuthMiddlewareStack
#from .routing import ws_urlpatterns
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sacado.settings")
django.setup()
application= get_default_application()
#application = ProtocolTypeRouter({
# Django's ASGI application to handle traditional HTTP requests
#"http": get_asgi_application() ,
