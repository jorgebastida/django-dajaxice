from django.conf.urls import url, include

from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

urlpatterns = [
    #Dajaxice URLS
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
]
