from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',  
    #Dajaxice URLS
	(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)
