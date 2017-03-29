from django.conf.urls import url
from .views import DajaxiceRequest

urlpatterns = [
    url(r'^(.+)/$', DajaxiceRequest.as_view(), name='dajaxice-call-endpoint'),
    url(r'', DajaxiceRequest.as_view(), name='dajaxice-endpoint'),
]
