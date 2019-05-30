"""Template to tag to handle cache busting."""
# https://stackoverflow.com/a/45338997 by Derrick Petzold
import os
import uuid
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(name='cache_bust')
def cache_bust():
    """If in debug mode, returns an UUID, otherwise project version.
    To be appended to e.g. CSS/JS files."""
    if settings.DEBUG:
        version = uuid.uuid1()
    else:
        version = os.environ.get('PROJECT_VERSION')
        if version is None:
            version = '1'

    return 'v={version}'.format(version=version)
