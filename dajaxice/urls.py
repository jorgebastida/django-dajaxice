try: 
    from django.conf.urls import url, patterns
except ImportError: 
    # for Django version less then 1.4
    from django.conf.urls.defaults import url, patterns
from .views import DajaxiceRequest
# This commit just to kick a rebuild, since travis somehow got hung up.

urlpatterns = patterns('dajaxice.views',
    url(r'^(.+)/$', DajaxiceRequest.as_view(), name='dajaxice-call-endpoint'),
    url(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
)
