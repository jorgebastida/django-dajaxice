import logging

from django import template
from django.middleware.csrf import get_token
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()

log = logging.getLogger('dajaxice')


@register.simple_tag(takes_context=True)
def dajaxice_js_import(context):
    request = context.get('request')
    if request:
        get_token(request)
    else:
        log.warning("The 'request' object must be accesible within the "
                    "context. You must add 'django.contrib.messages.context"
                    "_processors.request' to your TEMPLATE_CONTEXT_PROCESSORS "
                    "and render your views using a RequestContext.")

    url = staticfiles_storage.url('dajaxice/dajaxice.core.js')
    return '<script src="%s" type="text/javascript" charset="utf-8"></script>' % url
