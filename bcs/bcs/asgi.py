"""
ASGI config for bcs project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="bcs.settings")

application = get_asgi_application()
