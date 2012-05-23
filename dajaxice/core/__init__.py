from django.conf import settings

from Dajaxice import Dajaxice
from DajaxiceRequest import DajaxiceRequest
from Dajaxice import dajaxice_autodiscover


class DajaxiceConfig(object):

    default_config = {'DAJAXICE_MEDIA_PREFIX': 'dajaxice',
                      'DAJAXICE_DEBUG': False,
                      'DAJAXICE_NOTIFY_EXCEPTIONS': False,
                      'DAJAXICE_XMLHTTPREQUEST_JS_IMPORT': True,
                      'DAJAXICE_JSON2_JS_IMPORT': True,
                      'DAJAXICE_EXCEPTION': 'DAJAXICE_EXCEPTION'}

    def __getattr__(self, name):
        if name in self.default_config:
            if hasattr(settings, name):
                return getattr(settings, name)
            return self.default_config.get(name)
        return None

    def modules(self):
        return dajaxice_functions.modules

dajaxice_functions = Dajaxice()
dajaxice_config = DajaxiceConfig()
