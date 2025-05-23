import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fan_mmorpg_board.settings")

application = get_wsgi_application()
