"""
WSGI config for ITEnergy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from ITEnergy import bot
from ITEnergy.TelegramThread import TelegramThread

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ITEnergy.settings")

TelegramThread(bot)

application = get_wsgi_application()
