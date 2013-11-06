from django.conf.urls import patterns, url 
from .views import DajaxiceRequest

urlpatterns = patterns('dajaxice.views',
    url(r'^(.+)/$', DajaxiceRequest.as_view(), name='dajaxice-call-endpoint'),
    url(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
)
