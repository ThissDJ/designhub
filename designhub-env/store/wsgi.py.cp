import os
import sys
sys.stdout = sys.stderr

# Project root
root = '/home/designhub/webapps/designhub/designhub-env/store'
sys.path.insert(0, root)

# Packages from virtualenv
activate_this = '/home/designhub/webapps/designhub/designhub-env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from django.core.handlers.wsgi import WSGIHandler

os.environ['DJANGO_SETTINGS_MODULE'] = 'store.settings'
application = WSGIHandler()
