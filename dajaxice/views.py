import sys
import logging
import traceback

from django.utils import simplejson
from django.http import HttpResponse, Http404
from django.conf import settings

from dajaxice.exceptions import FunctionNotCallableError
from dajaxice.core import dajaxice_functions, dajaxice_config

log = logging.getLogger('dajaxice')

from django.views.generic.base import View


def safe_dict(d):
    """
    Recursively clone json structure with UTF-8 dictionary keys
    http://www.gossamer-threads.com/lists/python/bugs/684379
    """
    if isinstance(d, dict):
        return dict([(k.encode('utf-8'), safe_dict(v)) for k, v in d.iteritems()])
    elif isinstance(d, list):
        return [safe_dict(x) for x in d]
    else:
        return d


class DajaxiceRequest(View):

    def dispatch(self, request, name=None):

        if not name:
            raise Http404

        if dajaxice_functions.is_callable(name):

            function = dajaxice_functions.get(name)
            data = getattr(request, function.method).get('argv', '')

            if data != 'undefined':
                try:
                    data = safe_dict(simplejson.loads(data))
                except Exception:
                    data = {}
            else:
                data = {}

            try:
                response = function.call(request, **data)
            except Exception:
                if settings.DEBUG:
                    raise
                response = dajaxice_config.DAJAXICE_EXCEPTION

            return HttpResponse(response, mimetype="application/x-json")
        else:
            raise FunctionNotCallableError(name)

    """
    def notify_exception(self, request, exc_info):
        from django.conf import settings
        from django.core.mail import mail_admins

        subject = 'Error (%s IP): %s' % ((request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
        try:
            request_repr = repr(request)
        except:
            request_repr = "Request repr() unavailable"

        trace = '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
        message = "%s\n\n%s" % (trace, request_repr)
        mail_admins(subject, message, fail_silently=True)
    """
