# try:
#     from django.conf.urls import *
# except ImportError:
#     from django.conf.urls.defaults import patterns, url
from django.urls import re_path

from .views import DajaxiceRequest

# urlpatterns = patterns('dajaxice.views',
#    url(r'^(.+)/$', DajaxiceRequest.as_view(), name='dajaxice-call-endpoint'),
#    url(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
# )

urlpatterns = [
    re_path(r'^(.+)/$', DajaxiceRequest.as_view(),
            name='dajaxice-call-endpoint'),
    re_path(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
    ]
