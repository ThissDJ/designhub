import os

from django import template
from testshop import settings
register = template.Library()


@register.filter
def filename(value,arg=''):
    """Get basename of full-path. Return error if file not found."""
    filepath = os.path.join(os.path.join(settings.MEDIA_ROOT,settings.UPLOAD_URI),os.path.basename(value))
    if os.path.isfile(filepath):
        filepath = os.path.basename(filepath)
        [fname,filepath_ext] = os.path.splitext(filepath)
        return fname + arg + filepath_ext
    else:
        return 'No File'
